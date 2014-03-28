# -*- coding: utf-8 -*-
import logging 
import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _, string_concat

import settings as app_dist_settings
from models import IosApp


log = logging.getLogger(__name__)

class AppAdminForm(ModelForm):

	def clean(self):
		cleaned_data = super(AppAdminForm, self).clean()

		user = cleaned_data.get('user')
		groups = cleaned_data.get('groups')

		if not user and not groups:
			 raise ValidationError(_('Please assign a user or group to the app.'))

		return cleaned_data

class IosAppAdminForm(AppAdminForm):

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
			'/'.join(s.strip('/') for s in (Site.objects.get_current().domain, settings.MEDIA_URL, app_dist_settings.MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME, filename)),
			'</span>')