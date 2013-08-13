from os.path import join
from django.conf import settings

def get(key, default):
  return getattr(settings, key, default)

IOS = 'iOS'
IOS_PLIST = 'iOS Plist'
ANDROID = 'Android'
OS_CHOICES = (
    (IOS, 'iOS'),
    (ANDROID, 'Android'),
)

MOBILE_APP_DISTRIBUTION_CONTENT_TYPES = {
    IOS : 'application/octet-stream ipa',
    IOS_PLIST : 'text/xml plist',
    ANDROID : 'application/vnd.android.package-archive'
}

MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME = get('MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME', 'ios_apps')
MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME = get('MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME', 'android_apps')
MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH = join(settings.BASE_PATH, get('MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH', 'android'))

ENGLISH = 'en'
GERMAN = 'de'

LANGUAGES = (
	(ENGLISH, 'English'), 
	(GERMAN, 'Deutsch'),
)