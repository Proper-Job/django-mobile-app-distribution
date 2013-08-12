import logging

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import ugettext as _
from exceptions import MobileAppDistributionConfigurationException

import django_mobile_app_distribution.settings as app_dist_settings


log = logging.getLogger(__name__)

class App(models.Model):
	user = models.ForeignKey(User, related_name='apps', verbose_name=_('User'))
	name = models.CharField(max_length=200, verbose_name=_('App name'))
	comment = models.CharField(max_length=200, verbose_name=_('Comment'), blank=True, null=True)
	version = models.CharField(max_length=200, verbose_name=_('Version'))
	build_date = models.DateTimeField(verbose_name=_('Build date'))
	updatedAt = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)
	createdAt = models.DateTimeField(auto_now_add=True, editable=False)	

	def __unicode__(self):
		return self.name

class IosApp(App):

	file_name = models.CharField(max_length=200, verbose_name=_('File name'))
	operating_system = models.CharField( max_length=50, choices=app_dist_settings.OS_CHOICES, default=app_dist_settings.IOS, verbose_name=_('Operating system'), editable=False)
	app_binary = models.FileField(upload_to=app_dist_settings.MOBILE_APP_DISTRIBUTION_UPLOAD_TO_DIRECTORY_NAME, verbose_name=_('Ad Hoc ipa file'))
	app_plist = models.FileField(upload_to=app_dist_settings.MOBILE_APP_DISTRIBUTION_UPLOAD_TO_DIRECTORY_NAME, verbose_name=_('Ad Hoc plist'))

	def get_binary_url(self):
		if not self.app_binary:
			return None
		Site.objects.clear_cache()
		try:
			Site.objects.get_current()
		except Exception:
			raise MobileAppDistributionConfigurationException("The site framework's domain name is used to generate the plist and binary links.  Please configure your current site properly. Also make sure that the SITE_ID in your settings file matches the primary key of your current site.")

		return Site.objects.get_current().domain + self.app_binary.url
			

	def get_plist_url(self):
		if not self.app_plist:
			return None
		Site.objects.clear_cache()
		try:
			Site.objects.get_current()
		except Exception:
			raise MobileAppDistributionConfigurationException("The site framework's domain name is used to generate the plist and binary links.  Please configure your current site properly. Also make sure that the SITE_ID in your settings file matches the primary key of your current site.")
		return Site.objects.get_current().domain + self.app_plist.url

	class Meta:
		verbose_name = _('iOS App')
		verbose_name_plural = _('iOS Apps')
		ordering = ( 'name', 'operating_system', '-version', '-build_date',)


fs = FileSystemStorage(location=app_dist_settings.MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH)

class AndroidApp(App):
	operating_system = models.CharField( max_length=50, choices=app_dist_settings.OS_CHOICES, default=app_dist_settings.ANDROID, verbose_name=_('Operating system'), editable=False)
	app_binary = models.FileField(upload_to='apk', verbose_name=_('APK file'), storage=fs)

	class Meta:
		verbose_name = _('Android App')
		verbose_name_plural = _('Android Apps')
		ordering = ( 'name', 'operating_system', '-version', '-build_date',)

