# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import django_mobile_app_distribution.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_mobile_app_distribution', '0003_auto_20150807_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='androidapp',
            name='app_binary',
            field=models.FileField(upload_to=django_mobile_app_distribution.models.normalize_android_filename, storage=django.core.files.storage.FileSystemStorage(location='/Users/moritz/Alp-Phone/Projects/mobile_app_distribution/migrations_generator/migrations_generator/android'), verbose_name='APK file'),
        ),
    ]
