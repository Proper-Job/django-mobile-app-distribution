# -*- coding: utf-8 -*-
import logging
import os
from urlparse import urljoin
from unicodedata import normalize

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

import django_mobile_app_distribution.settings as app_dist_settings
from exceptions import MobileAppDistributionConfigurationException


log = logging.getLogger(__name__)


def normalize_filename(dirname, filename):
    filename = normalize('NFKD', filename).encode('ascii', 'ignore')
    filename = os.path.join(dirname, filename)
    return filename

def normalize_ios_filename(instance, filename):
    return normalize_filename(app_dist_settings.MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME, filename)

def normalize_android_filename(instance, filename):
    return normalize_filename(app_dist_settings.MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME, filename)


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    language = models.CharField(max_length=20, choices=app_dist_settings.LANGUAGES, default=app_dist_settings.ENGLISH)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Extended user info')
        verbose_name_plural = _('Extended user info')


class App(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, related_name='apps', verbose_name=_('User'))
    groups = models.ManyToManyField(Group, blank=True, null=True, related_name='apps', default=None, verbose_name=_('Groups'))
    name = models.CharField(max_length=200, verbose_name=_('App name'))
    comment = models.CharField(max_length=200, verbose_name=_('Comment'), blank=True, null=True)
    version = models.CharField(max_length=200, verbose_name=_('Bundle version'))
    updatedAt = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name


class IosApp(App):

    operating_system = models.CharField( max_length=50, choices=app_dist_settings.OS_CHOICES, default=app_dist_settings.IOS, verbose_name=_('Operating system'), editable=False)
    app_binary = models.FileField(upload_to=normalize_ios_filename, verbose_name=_('IPA file'))
    bundle_identifier = models.CharField(max_length=200, verbose_name=_('Bundle identifier'), default='', help_text=_('e.g. org.example.app'))

    def get_binary_url(self):
        if not self.app_binary:
            return None
        Site.objects.clear_cache()
        try:
            Site.objects.get_current()
        except Exception:
            raise MobileAppDistributionConfigurationException("The site framework's domain name is used to generate the plist and binary links.  Please configure your current site properly. Also make sure that the SITE_ID in your settings file matches the primary key of your current site.")

        return urljoin(Site.objects.get_current().domain, self.app_binary.url)


    def get_plist_url(self):
        Site.objects.clear_cache()
        current_site = None
        try:
            current_site = Site.objects.get_current()
        except Exception:
            raise MobileAppDistributionConfigurationException("The site framework's domain name is used to generate the plist and binary links.  Please configure your current site properly. Also make sure that the SITE_ID in your settings file matches the primary key of your current site.")

        return urljoin(current_site.domain, reverse('django_mobile_app_distribution_ios_app_plist', kwargs={'app_id': self.pk}))

    class Meta:
        verbose_name = _('iOS App')
        verbose_name_plural = _('iOS Apps')
        ordering = ('name', 'operating_system', '-version', '-updatedAt',)


fs = FileSystemStorage(location=app_dist_settings.MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH)


class AndroidApp(App):
    operating_system = models.CharField( max_length=50, choices=app_dist_settings.OS_CHOICES, default=app_dist_settings.ANDROID, verbose_name=_('Operating system'), editable=False)
    app_binary = models.FileField(upload_to=normalize_android_filename, verbose_name=_('APK file'), storage=fs)

    class Meta:
        verbose_name = _('Android App')
        verbose_name_plural = _('Android Apps')
        ordering = ( 'name', 'operating_system', '-version', '-updatedAt',)


def create_user_info(sender, instance, created, **kwargs):
    try:
        instance.userinfo
    except Exception:
        try:
            UserInfo.objects.create(user=instance)
        except Exception:
            # happens when creating a superuser when syncdb is run before the tables are installed
            pass

post_save.connect(create_user_info, sender=User)

