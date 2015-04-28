# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_mobile_app_distribution.models
from django.conf import settings
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='App name')),
                ('comment', models.CharField(max_length=200, null=True, verbose_name='Comment', blank=True)),
                ('version', models.CharField(max_length=200, verbose_name='Bundle version')),
                ('updatedAt', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AndroidApp',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_mobile_app_distribution.App')),
                ('operating_system', models.CharField(default=b'Android', verbose_name='Operating System', max_length=50, editable=False, choices=[(b'iOS', b'iOS'), (b'Android', b'Android')])),
                ('app_binary', models.FileField(upload_to=django_mobile_app_distribution.models.normalize_android_filename, storage=django.core.files.storage.FileSystemStorage(location=b'/Users/moritz/Alp-Phone/Projects/mobile_app_distribution/migrations_generator/migrations_generator/android'), verbose_name='APK file')),
            ],
            options={
                'ordering': ('name', 'operating_system', '-version', '-updatedAt'),
                'verbose_name': 'Android app',
                'verbose_name_plural': 'Android apps',
            },
            bases=('django_mobile_app_distribution.app',),
        ),
        migrations.CreateModel(
            name='IosApp',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_mobile_app_distribution.App')),
                ('operating_system', models.CharField(default=b'iOS', verbose_name='Operating System', max_length=50, editable=False, choices=[(b'iOS', b'iOS'), (b'Android', b'Android')])),
                ('app_binary', models.FileField(upload_to=django_mobile_app_distribution.models.normalize_ios_filename, verbose_name='IPA file')),
                ('bundle_identifier', models.CharField(default=b'', help_text='e.g. org.example.app', max_length=200, verbose_name='Bundle identifier')),
            ],
            options={
                'ordering': ('name', 'operating_system', '-version', '-updatedAt'),
                'verbose_name': 'iOS App',
                'verbose_name_plural': 'iOS Apps',
            },
            bases=('django_mobile_app_distribution.app',),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(default=b'en', max_length=20, choices=[(b'en', b'English'), (b'de', b'Deutsch')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extended user info',
                'verbose_name_plural': 'Extended user info',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='app',
            name='groups',
            field=models.ManyToManyField(related_name='apps', default=None, to='auth.Group', blank=True, null=True, verbose_name='Groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='user',
            field=models.ForeignKey(related_name='apps', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='User'),
            preserve_default=True,
        ),
    ]
