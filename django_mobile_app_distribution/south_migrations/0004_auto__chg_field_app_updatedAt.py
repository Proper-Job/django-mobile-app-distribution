# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'App.updatedAt'
        db.alter_column(u'django_mobile_app_distribution_app', 'updatedAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):

        # Changing field 'App.updatedAt'
        db.alter_column(u'django_mobile_app_distribution_app', 'updatedAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_mobile_app_distribution.androidapp': {
            'Meta': {'ordering': "(u'name', u'operating_system', u'-version', u'-updatedAt')", 'object_name': 'AndroidApp', '_ormbases': [u'django_mobile_app_distribution.App']},
            'app_binary': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'app_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_mobile_app_distribution.App']", 'unique': 'True', 'primary_key': 'True'}),
            'operating_system': ('django.db.models.fields.CharField', [], {'default': "u'Android'", 'max_length': '50'})
        },
        u'django_mobile_app_distribution.app': {
            'Meta': {'object_name': 'App'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "u'apps'", 'blank': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updatedAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'apps'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'django_mobile_app_distribution.iosapp': {
            'Meta': {'ordering': "(u'name', u'operating_system', u'-version', u'-updatedAt')", 'object_name': 'IosApp', '_ormbases': [u'django_mobile_app_distribution.App']},
            'app_binary': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'app_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_mobile_app_distribution.App']", 'unique': 'True', 'primary_key': 'True'}),
            'bundle_identifier': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200'}),
            'operating_system': ('django.db.models.fields.CharField', [], {'default': "u'iOS'", 'max_length': '50'})
        },
        u'django_mobile_app_distribution.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'en'", 'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['django_mobile_app_distribution']