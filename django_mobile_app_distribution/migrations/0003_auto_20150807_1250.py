# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_mobile_app_distribution.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_mobile_app_distribution', '0002_auto_20150730_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='iosapp',
            name='display_image',
            field=models.ImageField(default='', help_text='57x57 PNG', upload_to=django_mobile_app_distribution.models.normalize_image_filename, blank=True),
        ),
        migrations.AddField(
            model_name='iosapp',
            name='full_size_image',
            field=models.ImageField(default='', help_text='512x512 PNG', upload_to=django_mobile_app_distribution.models.normalize_image_filename, blank=True),
        ),
    ]
