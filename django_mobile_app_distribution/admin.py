# -*- coding: utf-8 -*-
import logging

from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
from django_mobile_app_distribution import settings as _settings
from django_mobile_app_distribution.models import IosApp, AndroidApp

from forms import IosAppAdminForm, AppAdminForm
from models import UserInfo


log = logging.getLogger(__name__)

###################################################################################
# Avoid overriding the User in case other apps already do that, deprecated in 0.1.2
###################################################################################

# Define an inline admin descriptor for UserInfo model
# which acts a bit like a singleton
# class UserInfoInline(admin.StackedInline):
#     model = UserInfo
#     can_delete = False

# class UserAdmin(admin.ModelAdmin):
#     inlines = (UserInfoInline, )


class UserInfoAdmin(admin.ModelAdmin):
    model = UserInfo
    list_display = ['user', 'language']
    list_editable = ['language']

class NotifiableModelAdmin(admin.ModelAdmin):
    actions = ['notify_client']
    search_fields = ['name', 'user__username', 'groups__name', 'comment']

    def notify_client(self, request, queryset):
        for app in queryset.all():
            recipients = []

            if app.user and app.user.email:
                recipients.append(app.user.email)

            if app.groups.count() > 0:
                group_users = User.objects.filter(groups__in=app.groups.all())
                for user in group_users:
                    if user.email and user.email not in recipients:
                        recipients.append(user.email)

            if recipients:
                recipient_count = len(recipients)
                if request.user.email and request.user.email not in recipients:
                    recipients.append(request.user.email)

                try:
                    # Try and send email in client's preferred language
                    # This doesn't make much sense for apps distributed to groups
                    # hence the catch all except clause
                    lang = app.user.userinfo.language
                    translation.activate(lang)
                except Exception:
                    pass

                data = {
                    'email_link_color_hex' : _settings.EMAIL_LINK_COLOR_HEX,
                    'app_name' : app.name,
                    'app_version' : app.version,
                    'os': app.operating_system,
                    'download_url' : '/'.join(s.strip('/') for s in (get_current_site(request).domain, reverse('django_mobile_app_distribution_index')))
                }

                email = EmailMultiAlternatives()
                email.bcc = recipients
                email.subject = _('Version %(app_version)s of %(app_name)s for %(os)s is available for download') % data
                email.body = _('Version %(app_version)s of %(app_name)s for %(os)s is available for download.\nPlease visit %(download_url)s to install the app.') % data
                email.attach_alternative(render_to_string('django_mobile_app_distribution/email_notification.html', data), 'text/html')

                # Reset to system language
                translation.deactivate()

                email.send(fail_silently=False)
                messages.add_message(
                    request,
                    messages.INFO, ungettext_lazy(
                        '%(recipient_count)s user was notified of %(app_name)s %(app_version)s availability.',
                        '%(recipient_count)s users were notified of %(app_name)s %(app_version)s availability.',
                        recipient_count) % {
                        'recipient_count' : recipient_count,
                        'app_name' : app.name,
                        'app_version': app.version
                        },
                    fail_silently=True)
            else:
                messages.add_message(request, messages.ERROR, _('Nobody was notified by email because nobody\'s email address is set.'), fail_silently=True)
    notify_client.short_description = _('Notify clients of app availability')

    def user_display_name(self, instance):
        if instance.user:
            return instance.user.username
        else:
            return ''
    user_display_name.short_description = _('User')
    user_display_name.admin_order_field = 'user'

    def groups_display_name(self, instance):
        if instance.groups.count() > 0:
            return ", ".join(str(group) for group in instance.groups.all())
        else:
            return ''
    groups_display_name.short_description = _('Groups')

class IosAppAdmin(NotifiableModelAdmin):

    form = IosAppAdminForm
    list_display = ('name', 'user_display_name', 'groups_display_name', 'version', 'comment', 'updatedAt')
    filter_horizontal = ['groups']

    fieldsets = (
        (_('App info'), {
            'fields': ('user', 'groups', 'name', 'version', 'bundle_identifier', 'app_binary', 'comment')
        }),
    )

class AndroidAppAdmin(NotifiableModelAdmin):

    form = AppAdminForm
    list_display = ('name', 'user_display_name', 'groups_display_name', 'version', 'comment', 'updatedAt')
    filter_horizontal = ['groups']

    fieldsets = (
        (_('App info'), {
            'fields': ('user', 'groups', 'name', 'version', 'app_binary', 'comment')
        }),
    )

admin.site.register(IosApp, IosAppAdmin)
admin.site.register(AndroidApp, AndroidAppAdmin)
admin.site.register(UserInfo, UserInfoAdmin)

###################################################################################
# Avoid overriding the User in case other apps already do that, deprecated in 0.1.2
###################################################################################
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
