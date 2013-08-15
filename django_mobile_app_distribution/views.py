import logging
import os.path
from itertools import chain
from operator import attrgetter
from os.path import basename

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseForbidden
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

	ios_apps = IosApp.objects.filter(user_id__exact=request.user.id)
	android_apps = AndroidApp.objects.filter(user_id__exact=request.user.id)
	apps = list(chain(ios_apps, android_apps))
	apps.sort(key=attrgetter('build_date'), reverse=True)
	apps.sort(key=attrgetter('version'), reverse=True)
	apps.sort(key=attrgetter('operating_system'))
	apps.sort(key=attrgetter('name'))	
	
	return render(request, 'django_mobile_app_distribution/app_list.html', {
		'apps' : apps,
		'ios_identifier' : app_dist_settings.IOS,
		'site_url' : get_current_site(request).domain
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
	except AndroidApp.DoesNotExist:
		return HttpResponse('App does not exist', status=404)
	
	if android_app.user.id != request.user.id:
		return HttpResponseForbidden('This is not your app')

	filename = os.path.join(app_dist_settings.MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH, android_app.app_binary.name)

	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper)
	response['Content-Length'] = os.path.getsize(filename)
	response['Content-Type'] = app_dist_settings.MOBILE_APP_DISTRIBUTION_CONTENT_TYPES[android_app.operating_system]
	response['Content-Disposition'] = 'inline; filename=%s' % basename(filename)
	return response

