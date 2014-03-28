#Django Mobile App Distribution

Django Mobile App Distribution is a Django app that allows you to distribute iPhone, iPad and Android apps over the air to your clients.

It is made up of 2 components:

* A Django Admin interface that allows you to upload and assign apps to users.
* A mobile optimized, login protected download area where your clients can download apps that were associated with their login credentials.


#Installation

1. ``pip install django-mobile-app-distribution``
2. Add ``django_mobile_app_distribution`` to your ``INSTALLED_APPS`` list in your project's settings.py. Make sure it comes after ``django.contrib.admin`` so the admin login and logout templates are properly overridden.
3. Add ``django.contrib.sites`` to the list of ``INSTALLED_APPS`` in your project's settings.py.
4. Add ``south`` to the list of ``INSTALLED_APPS`` in your project's settings.py.
5. Enable the [messages framework][message_framework]
6. Run ``python manage.py syncdb``.
7. Run ``python manage.py migrate django_mobile_app_distribution``.
8. Run ``python manage.py collectstatic``
9. If you like things tidy you can install [django-cleanup][django_cleanup], which removes uploaded files when the associated models are deleted.
10. Make sure the ``android/android_apps`` folder on the same level as your project's settings.py is readable and writable by your webserver.
	*  If your webserver cannot create them for you, you have to create them by hand.  See Security considerations below for more information.
11. Include ``urls.py`` into your project's urls.py file at the mount point of your choosing (see below).  This will be where your client downloads her apps.
12. Include ``auth_urls.py`` into your project's urls.py (see below).
13. Add [LOGIN_REDIRECT_URL][login_redirect_url] to your project's settings.py.  This is the URL you chose in step 7.  If you're using the example below, set it to ``/distribute/``.
14. Add ``BASE_PATH`` to your project's settings.py, e.g. ``import os.path BASE_PATH = os.path.dirname(__file__)``. In order to create an Android upload folder on the same level as your project's settings.py this has to be set.
15. Add the [SITE_ID][site_id] value in your project's settings.py to the primary key of the Site object that represents your site.
16. Login to the Django Admin and add your server's URL to the Site object's domain name (create one if necessary). On the development server this would be ``http://127.0.0.1:8000/``

[site_id]: https://docs.djangoproject.com/en/1.4/ref/settings/#site-id
[django_cleanup]: https://github.com/un1t/django-cleanup
[login_redirect_url]: https://docs.djangoproject.com/en/1.4/ref/settings/#login-redirect-url
[message_framework]: https://docs.djangoproject.com/en/1.5/ref/contrib/messages/

	
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
* Choose the user (your client)
* Add App Name and Version, Comment and Created On information
* **DO NOT CHANGE THE FILENAME**
* Open Xcode
* In Xcode export your app as an archive: **Product > Archive**
	* Make sure you have got your provisioning right and your signing with a distribution certificate
* Go to **Organizer > Archives**
* Select your archive and hit **Distribute**
* Choose **Save for Enterprise or Ad-Hoc deployment**
* Choose your codesign identity
* In the save dialog check the checkbox at the bottom **Save for Enterprise Distribution**
* From your browser copy the file name (something like 10c6bfe096724504.ipa) into the file name field of the Xcode save dialog
* From your browser copy the **Ad Hoc URL** (in red) into the **Application URL** field of the Xcode save dialog
* Add the App's Name into the **Title** field of the Xcode save dialog
* Choose a folder to save to and remember it
* In Xcode hit **Save**
* In your browser upload the IPA file and the Plist into the respective fields
* On the download page you should be able to download and install over the air with properly provisioned devices



![Screenshot][xcode]

[xcode]: http://alp-phone.ch/wp-content/uploads/2013/08/MobileAppDistribution.jpg



#Overriding the login template logo

In order to place your own logo on the login screen replace the following file with an image of the size 400x200 pixel:

**static/django_mobile_app_distribution/images/logo@2x.png**


#Migrate from 0.1.x to 0.2 using South

Version 0.2 introduced [South][south_link] as a dependency, because the database structure changed.
If you need to migrate from version 0.1.x to 0.2 follow these instructions.  A clean install of version >= 0.2 doesn't need to do this.

	1. ``pip install django-mobile-app-distribution==0.2``
	2. Add south to the list of INSTALLED_APPS
	3. python manage.py syncdb
	4. python manage.py migrate django_mobile_app_distribution 0001 --fake
	5. python manage.py migrate django_mobile_app_distribution


[south_link]: http://south.readthedocs.org/en/latest/index.html
