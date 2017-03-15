# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from django_mobile_app_distribution import views

urlpatterns = [
    url(r'^$', views.index, name='django_mobile_app_distribution_index'),
    url(r'^apk/(?P<app_id>\d{1,10})$', views.send_apk, name='django_mobile_app_distribution_send_apk'),
    url(r'^plist/(?P<app_id>\d{1,10})\.plist$', views.ios_app_plist, name='django_mobile_app_distribution_ios_app_plist'),
]
