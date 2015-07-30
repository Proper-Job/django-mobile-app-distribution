# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_mobile_app_distribution.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('django_mobile_app_distribution', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='androidapp',
            options={'verbose_name': 'Android App', 'verbose_name_plural': 'Android Apps', 'ordering': ('name', 'operating_system', '-version', '-updatedAt')},
        ),
        migrations.AlterField(
            model_name='androidapp',
            name='app_binary',
            field=models.FileField(verbose_name='APK file', upload_to=django_mobile_app_distribution.models.normalize_android_filename, storage=django.core.files.storage.FileSystemStorage(location='/Users/moritz/Alp-Phone/Projects/mobile_app_distribution/ota_ad_hoc_management/ota_ad_hoc_management/android')),
        ),
        migrations.AlterField(
            model_name='androidapp',
            name='operating_system',
            field=models.CharField(verbose_name='Operating system', default='Android', max_length=50, choices=[('iOS', 'iOS'), ('Android', 'Android')], editable=False),
        ),
        migrations.AlterField(
            model_name='app',
            name='groups',
            field=models.ManyToManyField(verbose_name='Groups', default=None, blank=True, to='auth.Group', related_name='apps'),
        ),
        migrations.AlterField(
            model_name='app',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='iosapp',
            name='bundle_identifier',
            field=models.CharField(verbose_name='Bundle identifier', default='', max_length=200, help_text='e.g. org.example.app'),
        ),
        migrations.AlterField(
            model_name='iosapp',
            name='operating_system',
            field=models.CharField(verbose_name='Operating system', default='iOS', max_length=50, choices=[('iOS', 'iOS'), ('Android', 'Android')], editable=False),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='language',
            field=models.CharField(default='en', max_length=20, choices=[('en', 'English'), ('de', 'Deutsch')]),
        ),
    ]
