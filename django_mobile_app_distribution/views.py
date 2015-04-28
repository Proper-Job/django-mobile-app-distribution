# -*- coding: utf-8 -*-
import logging
import os.path
from itertools import chain
from operator import attrgetter
from os.path import basename

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render
from django.utils import translation

import settings as app_dist_settings
from models import IosApp, AndroidApp, UserInfo


log = logging.getLogger(__name__)


@login_required
def index(request):
    try:
        # Activate client's language preference
        lang = request.user.userinfo.language
        translation.activate(lang)
    except UserInfo.DoesNotExist:
        pass

    ios_user_apps = IosApp.objects.filter(user_id__exact=request.user.id)
    android_user_apps = AndroidApp.objects.filter(user_id__exact=request.user.id)
    apps = list(chain(ios_user_apps, android_user_apps))

    ios_group_apps = IosApp.objects.filter(groups__in=request.user.groups.all())
    android_group_apps = AndroidApp.objects.filter(groups__in=request.user.groups.all())
    group_apps = list(chain(ios_group_apps, android_group_apps))
    for group_app in group_apps:
        if group_app not in apps:
            apps.append(group_app)

    apps.sort(key=attrgetter('updatedAt'), reverse=True)
    apps.sort(key=attrgetter('version'), reverse=True)
    apps.sort(key=attrgetter('operating_system'), reverse=True) # let iOS come first
    apps.sort(key=attrgetter('name'))

    return render(request, 'django_mobile_app_distribution/app_list.html', {
        'apps': apps,
        'ios_identifier': app_dist_settings.IOS,
        'site_url': get_current_site(request).domain
        })


@login_required
def send_apk(request, app_id):
    """
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """
    android_app = None
    try:
        android_app = AndroidApp.objects.get(pk=app_id)
    except (AndroidApp.DoesNotExist, MultipleObjectsReturned):
        return HttpResponse('App does not exist', status=404)

    authenticated = False
    if android_app.user:
        if android_app.user.id == request.user.id:
            authenticated = True

    if not authenticated:
        app_group_ids = android_app.groups.all().values_list('pk', flat=True)
        app_group_ids = list(map(long, app_group_ids))
        for user_group in request.user.groups.all():
            user_group_id = long(user_group.id)
            if user_group_id in app_group_ids:
                authenticated = True
                break

    if not authenticated:
        return HttpResponseForbidden('This is not your app')

    filename = os.path.join(app_dist_settings.MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH, android_app.app_binary.name)

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Type'] = app_dist_settings.MOBILE_APP_DISTRIBUTION_CONTENT_TYPES[android_app.operating_system]
    response['Content-Disposition'] = 'inline; filename=%s' % basename(filename)
    return response


def ios_app_plist(request, app_id):

    ios_app = None
    try:
        ios_app = IosApp.objects.get(pk=app_id)
    except (IosApp.DoesNotExist, MultipleObjectsReturned):
        raise Http404

    from . import settings as mad_settings
    plist_string = mad_settings.IOS_PLIST_BLUEPRINT
    plist_string = plist_string.replace(mad_settings.PLIST_APP_URL, ios_app.get_binary_url())
    plist_string = plist_string.replace(mad_settings.PLIST_BUNDLE_IDENTIFIER, ios_app.bundle_identifier)
    plist_string = plist_string.replace(mad_settings.PLIST_BUNDLE_VERSION, ios_app.version)
    plist_string = plist_string.replace(mad_settings.PLIST_APP_TITLE, ios_app.name)

    return HttpResponse(plist_string, content_type=mad_settings.MOBILE_APP_DISTRIBUTION_CONTENT_TYPES[mad_settings.IOS_PLIST])