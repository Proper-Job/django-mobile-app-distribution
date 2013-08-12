from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
                       url(r'^login/$',
                           auth_views.login,
                           {'template_name': 'django_mobile_app_distribution/login.html'},
                           name='auth_login'),
                       url(r'^logout/$',
                           auth_views.logout,
                           {'template_name': 'django_mobile_app_distribution/logout.html'},
                           name='auth_logout'),
)