# -*- coding: utf-8 -*-
import logging 
import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _, string_concat

import settings as app_dist_settings
from models import IosApp
import posixpath


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
