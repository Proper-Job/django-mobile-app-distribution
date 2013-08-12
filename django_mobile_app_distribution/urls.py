from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'django_mobile_app_distribution.views.index', name='django_mobile_app_distribution_index'),
    url(r'^apk/(?P<app_id>\d{1,10})$', 'django_mobile_app_distribution.views.send_apk', name='django_mobile_app_distribution_send_apk'),
)