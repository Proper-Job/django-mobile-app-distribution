import logging
import uuid

from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.forms import ModelForm
from django.utils.translation import ugettext as _, string_concat
from ota_manager.models import IosApp, AndroidApp


log = logging.getLogger(__name__)

class IosAppAdminForm(ModelForm):

	class Meta:
		model = IosApp

	def __init__(self, *args, **kwargs):
		super(IosAppAdminForm, self).__init__(*args, **kwargs)
		filename = None
		try:
			app = kwargs['instance']
			filename = app.file_name
		except KeyError:
			hex = uuid.uuid4().hex[:16]
			filename = hex + '.ipa'
			self.fields['file_name'].initial = filename
		
		self.fields['file_name'].help_text = string_concat(
			'<span style=color:red;>',
			_("Don't change this file name!"),
			'</span><br />',
			_('Paste the file name and Ad Hoc URL into the Xcode Enterprise Ad Hoc dialog.'),
			'<br />',
			_('File name:'),
			' ',
			'<span style=color:red;>',
			filename,
			'</span><br />',
			_('Ad Hoc URL:'),
			' ',
			'<span style=color:red;>',
			'/'.join(s.strip('/') for s in (Site.objects.get_current().domain, settings.MEDIA_URL, settings.MOBILE_APP_DISTRIBUTION_UPLOAD_TO_DIRECTORY_NAME, filename)),
			'</span>')

class IosAppAdmin(admin.ModelAdmin):

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

class AndroidAppAdmin(admin.ModelAdmin):
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
