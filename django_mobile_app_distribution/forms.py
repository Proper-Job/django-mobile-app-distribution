# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class AppAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(AppAdminForm, self).clean()

        user = cleaned_data.get('user')
        groups = cleaned_data.get('groups')

        if not user and not groups:
            raise ValidationError(_('Please assign a user or group to the app.'))

        return cleaned_data
