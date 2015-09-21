# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
    IOS: 'application/octet-stream ipa',
    IOS_PLIST: 'text/xml plist',
    ANDROID: 'application/vnd.android.package-archive'
}

MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME = get(
    'MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME',
    'ios_apps'
)
MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME = get(
    'MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME',
    'android_apps'
)
MOBILE_APP_DISTRIBUTION_APP_ICON_DIRECTORY_NAME = get(
    'MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME',
    'app_icons'
)
MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH = join(
    settings.BASE_PATH,
    get('MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH', 'android')
)

EMAIL_LINK_COLOR_HEX = '#267d87'

ENGLISH = 'en'
GERMAN = 'de'

LANGUAGES = (
    (ENGLISH, 'English'),
    (GERMAN, 'Deutsch'),
)

PLIST_APP_URL = '__app_url__'
PLIST_BUNDLE_IDENTIFIER = '__bundle_identifier__'
PLIST_BUNDLE_VERSION = '__bundle_version__'
PLIST_APP_TITLE = '__app_title__'
PLIST_DISPLAY_IMAGE = '__display_image'
PLIST_FULL_SIZE_IMAGE = '__full_size_image'

IOS_PLIST_BLUEPRINT = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>{url}</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>{bundle_id}-ios8</string>
                <key>bundle-version</key>
                <string>{bundle_version}</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>{app_title}</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
""".format(
    url=PLIST_APP_URL,
    bundle_id=PLIST_BUNDLE_IDENTIFIER,
    bundle_version=PLIST_BUNDLE_VERSION,
    app_title=PLIST_APP_TITLE
)

# Docs: http://help.apple.com/deployment/ios/#/apda0e3426d7
IOS_PLIST_BLUEPRINT_IOS9 = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>{url}</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>display-image</string>
                    <key>url</key>
                    <string>{display_image}</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>full-size-image</string>
                    <key>url</key>
                    <string>{full_size_image}</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>{bundle_id}</string>
                <key>bundle-version</key>
                <string>{bundle_version}</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>{app_title}</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
""".format(
    url=PLIST_APP_URL,
    bundle_id=PLIST_BUNDLE_IDENTIFIER,
    bundle_version=PLIST_BUNDLE_VERSION,
    app_title=PLIST_APP_TITLE,
    display_image=PLIST_DISPLAY_IMAGE,
    full_size_image=PLIST_FULL_SIZE_IMAGE
)
