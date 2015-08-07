#Django Mobile App Distribution

Django Mobile App Distribution is a Django app that allows you to distribute iPhone, iPad and Android apps over the air to your clients.

It is made up of 2 components:

* A Django Admin interface that allows you to upload and assign apps to users.
* A mobile optimized, login protected download area where your clients can download apps that were associated with their login credentials.
* Supports Python 2.7, 3 (tested on 3.4.3) and Django >= 1.7.

#Installation Django >= 1.7

- ``pip install django-mobile-app-distribution``
- Add ``django_mobile_app_distribution`` to your ``INSTALLED_APPS`` list in your project's settings.py. Make sure it comes after ``django.contrib.admin`` so the admin login and logout templates are properly overridden.
- Add ``django.contrib.sites`` to the list of ``INSTALLED_APPS`` in your project's settings.py.
- Enable the [messages framework][message_framework_17]
- Make sure you have set [MEDIA_ROOT][media_root_17], [MEDIA_URL][media_url_17], [STATIC_URL][static_url_17] and [STATIC_ROOT][static_root_17].
- Run ``python manage.py migrate``
- Run ``python manage.py collectstatic``
- If you like things tidy you can install [django-cleanup][django_cleanup_17], which removes uploaded files when the associated models are deleted.
- Make sure the ``android/android_apps`` folder on the same level as your project's settings.py is readable and writable by your webserver.
	*  If your webserver cannot create them for you, you have to create them by hand.  See Security considerations below for more information.
- Include ``urls.py`` into your project's urls.py file at the mount point of your choosing (see below).  This will be where your client downloads her apps.
- Include ``auth_urls.py`` into your project's urls.py (see below).
- Add [LOGIN_REDIRECT_URL][login_redirect_url_17] to your project's settings.py.  This is the URL you chose in step 7.  If you're using the example below, set it to ``/distribute/``.
- Add ``BASE_PATH`` to your project's settings.py, e.g. ``import os.path BASE_PATH = os.path.dirname(__file__)``. In order to create an Android upload folder on the same level as your project's settings.py this has to be set.
- Add the [SITE_ID][site_id_17] value in your project's settings.py to the primary key of the Site object that represents your site.
- Login to the Django Admin and add your server's URL to the Site object's domain name (create one if necessary). On the development server this would be ``http://127.0.0.1:8000/``

[site_id_17]: https://docs.djangoproject.com/en/1.7/ref/settings/#site-id
[django_cleanup_17]: https://github.com/un1t/django-cleanup
[login_redirect_url_17]: https://docs.djangoproject.com/en/1.7/ref/settings/#login-redirect-url
[message_framework_17]: https://docs.djangoproject.com/en/1.7/ref/contrib/messages/
[media_root_17]: https://docs.djangoproject.com/en/1.7/ref/settings/#media-root
[media_url_17]: https://docs.djangoproject.com/en/1.7/ref/settings/#media-url
[static_root_17]: https://docs.djangoproject.com/en/1.7/ref/settings/#static-root
[static_url_17]: https://docs.djangoproject.com/en/1.7/ref/settings/#static-url

#URL setup

Inside your project's `urls.py`

	from django.conf.urls import patterns, include, url
	from django.contrib import admin
	admin.autodiscover()

	urlpatterns = patterns('',
		url(r'^admin/', include(admin.site.urls)),
		url(r'^distribute/', include('django_mobile_app_distribution.urls')),
		url(r'^accounts/', include('django_mobile_app_distribution.auth_urls')),
	)


Inside your project's `settings.py` file

	import os.path
	BASE_PATH = os.path.dirname(__file__)
	LOGIN_REDIRECT_URL = '/distribute/'
	SITE_ID = 1

#Security considerations

By default iOS apps are uploaded to a folder called ``ios_apps`` within your ``MEDIA_ROOT``.
This should generally be safe enough as Ad Hoc iOS apps are provisioned to run on a limited number of devices.

On Android however a hijacked signed APK file could be redistributed against your client's wishes which is to be avoided at all cost.
To this end Android apps are uploaded with a custom instance of ``FileSystemStorage``. By default, Android apps are uploaded to a folder called ``android`` on the same level as your project's settings.py.  The default upload path within the ``android`` folder is ``android_apps``.
You can change the default upload and file storage paths with the following directives in your project's settings.py:

* `MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME`
* `MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME`
* `MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH`

.. note:: Make sure the ``android/android_apps`` folder is readable and writable by your webserver, but not served by your webserver.

#Notify clients of available app downloads by email

Django Mobile App Distribution exposes an Admin Action that allows you to notify your clients once you've uploaded and app.
An email message is generated that contains a link to the download page.
In order for email messaging to work you need to set the following fields in your settings.py module:

* [EMAIL_HOST][EMAIL_HOST]
* [EMAIL_PORT][EMAIL_PORT]
* [EMAIL_HOST_USER][EMAIL_HOST_USER]
* [EMAIL_HOST_PASSWORD][EMAIL_HOST_PASSWORD]
* [EMAIL_USE_TLS][EMAIL_USE_TLS]
* [DEFAULT_FROM_EMAIL][DEFAULT_FROM_EMAIL]

[EMAIL_HOST]: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST
[EMAIL_PORT]: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_PORT
[EMAIL_HOST_USER]: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST_USER
[EMAIL_HOST_PASSWORD]: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST_PASSWORD
[EMAIL_USE_TLS]: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_USE_TLS
[DEFAULT_FROM_EMAIL]: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-DEFAULT_FROM_EMAIL


#Usage

1. Create a Django Admin User object that represents your client.
2. Make sure your clients can't login to the Django Admin Interface by unchecking the ``Staff status`` and ``Superuser status`` fields.
3. Assign a group membership to the user if you want to distribute your apps to a group of users.
4. Enter your client's email address if you want to be able to notify him or her of the availability of new apps.
5. After you save a user object the Django_mobile_app_distribution in the admin interface exposes an extended user info object that allows you to change the correspondence language for that user.
6. Create iOS or Android Apps to your liking.
7. Use the admin action in the change list to notify users of the availability of new apps.

#Android specifics

In case you get a permission denied error when uploading an Android APK, make sure that the ``android/android_apps`` folder on the same level as your project's settings.py is writable by your webserver.


#Export your iOS app for *Over the Air* distribution

* In your browser log into the Django Admin and navigate to **Django_mobile_app_distribution > IOS Apps**
* Create a new iOS app.
* Choose a user or group
* Add app name, bundle version, bundle identifier and comment
* Open Xcode
* In Xcode export your app as an archive: **Product > Archive**
	* Make sure you have got your provisioning right and your signing with a distribution certificate
* Go to **Organizer > Archives**
* Select your archive and hit **Export**
* Choose **Save for Enterprise or Ad-Hoc deployment**
* Choose your codesign identity
* In Xcode hit **Export**
* Choose a folder to save to and remember it
* In your browser upload the IPA file into the respective field
* On the download page you should be able to download and install over the air with properly provisioned devices


#Customizing the default color scheme

The frontend templates make use of the Zurb Foundation CSS framework 5.5.1.  
In line with foundation's customization rules there is an ``app.css`` file you can override to customize the default color scheme.
To do that create the following folder inside one of your own apps:

**static/django_mobile_app_distribution/css/**

Make sure your app comes before ``django_mobile_app_distribution`` in the list of ``INSTALLED_APPS``.
Inside that folder create a file called ``app.css``. There you can do custom styling, for instance:

	a {
	    color: black;
	}

	button, .button {
	    background-color: black;
	}

	button:hover, button:focus, .button:hover, .button:focus {
	    background-color: gray;
	}


