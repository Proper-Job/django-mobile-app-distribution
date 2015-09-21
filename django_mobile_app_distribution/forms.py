# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from django_mobile_app_distribution.models import IosApp, AndroidApp

logger = logging.getLogger(__name__)


class AppAdminForm(ModelForm):
    def clean(self):
        cleaned_data = super(AppAdminForm, self).clean()

        user = cleaned_data.get('user')
        groups = cleaned_data.get('groups')

        if not user and not groups:
            raise ValidationError(_('Please assign a user or group to the app.'))

        return cleaned_data


class iOSAppAdminForm(AppAdminForm):
    class Meta:
        model = IosApp
        fields = '__all__'

    def clean(self):
        cleaned_data = super(AppAdminForm, self).clean()

        display_image = cleaned_data.get('display_image')
        full_size_image = cleaned_data.get('full_size_image')

        if (display_image or full_size_image) and not (display_image and full_size_image):
            error = ValidationError(_('Please provide a display and a full size image.'))
            self.add_error('display_image', error)
            self.add_error('full_size_image', error)

        return cleaned_data


class AndroidAppAdminForm(AppAdminForm):
    class Meta:
        model = AndroidApp
        fields = '__all__'
