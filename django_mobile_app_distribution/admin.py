# -*- coding: utf-8 -*-
import logging

from django.contrib import admin, messages
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django_mobile_app_distribution.models import IosApp, AndroidApp

from forms import IosAppAdminForm
from models import UserInfo
from django.utils import translation


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

	def notify_client(self, request, queryset):
		for app in queryset.all():
			if app.user.email:
				try:
					# Send email in client's preferred language
					lang = app.user.userinfo.language
					translation.activate(lang)
				except UserInfo.DoesNotExist:
					pass
				email = EmailMessage()
				email.subject = _('Version %(app_version)s of %(app_name)s for %(os)s is available for download') % {
				'app_name' : app.name, 
				'app_version' : app.version, 
				'os': app.operating_system
				}
				email.body = _('Version %(app_version)s of %(app_name)s for %(os)s is available for download.\nPlease visit %(download_url)s to install your app.') % {
				'app_name' : app.name, 
				'app_version' : app.version, 
				'os': app.operating_system,
				'download_url' : '/'.join(s.strip('/') for s in (get_current_site(request).domain, reverse('django_mobile_app_distribution_index')))
				}
				
				# Reset to system language
				translation.deactivate()

				email.to = [app.user.email]
				email.send(fail_silently=False)
				messages.add_message(request, messages.INFO, _('The user %(user_name)s was notified of %(app_name)s %(app_version)s availability.') % {'user_name' :app.user.username, 'app_name' : app.name, 'app_version': app.version} , fail_silently=True)
			else:
				messages.add_message(request, messages.ERROR, _('The user %s does not have an email address. Please add an email address and try again.') % app.user.username, fail_silently=True)
	notify_client.short_description = _('Notify clients of app availability')

class IosAppAdmin(NotifiableModelAdmin):

	form = IosAppAdminForm
	list_display = ('name', 'user', 'version', 'comment', 'build_date' )

	fieldsets = (
		(_('App info'), {
			'fields': ('user', 'name', 'version', 'comment')
		}),
		(_('Binary info'), {
			'fields': ('file_name', 'build_date', 'app_binary', 'app_plist')
		}),
	)

class AndroidAppAdmin(NotifiableModelAdmin):
	list_display = ('name', 'user', 'version', 'comment', 'build_date' )

	fieldsets = (
		(_('App info'), {
			'fields': ('user', 'name', 'version', 'comment')
		}),
		(_('Binary info'), {
			'fields': ('build_date', 'app_binary')
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
