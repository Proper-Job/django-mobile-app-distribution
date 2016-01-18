# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
import django_mobile_app_distribution.settings as app_dist_settings

@deconstructible
class CustomFileSystemStorage(FileSystemStorage):

    def __init__(self, location=None, base_url=None, file_permissions_mode=None, directory_permissions_mode=None):
        super(CustomFileSystemStorage, self).__init__(
                app_dist_settings.MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH,
                base_url,
                file_permissions_mode,
                directory_permissions_mode
        )
