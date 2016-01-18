# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_mobile_app_distribution.storage
import django_mobile_app_distribution.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_mobile_app_distribution', '0004_auto_20150921_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='androidapp',
            name='app_binary',
            field=models.FileField(upload_to=django_mobile_app_distribution.models.normalize_android_filename, verbose_name='APK file', storage=django_mobile_app_distribution.storage.CustomFileSystemStorage()),
        ),
    ]
