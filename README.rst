Django Mobile App Distribution
==============================

Django Mobile App Distribution is a Django app that allows you to distribute iPhone, iPad and Android apps over the air to your clients.

It is made up of 2 components:

* A Django Admin interface that allows you to upload and assign apps to users.
* A mobile optimized, login protected download area where your clients can download apps that were associated with their login credentials.


Installation
------------

1. ``pip install django-mobile-app-distribution``
2. Add ``django_mobile_app_distribution`` to your ``INSTALLED_APPS`` list in your project's settings.py. Make sure it comes after ``django.contrib.admin`` so the admin login and logout templates are properly overridden.
3. Run ``python manage.py syncdb``.
4. Run ``python manage.py collectstatic``
5. If you like things tidy you can install `django-cleanup`_, which removes uploaded files when the associated models are deleted.
6. Make sure the ``android/android_apps`` folder on the same level as your ``MEDIA_ROOT`` is readable and writable by your webserver.
	*  If your webserver cannot create them for you, you have to create them by hand.  See Security considerations below for more information.
7. Include ``urls.py`` into your project's urls.py file at the mount point of your choosing (see below).  This will be where your client downloads her apps.
8. Include ``auth_urls.py`` into your project's urls.py (see below).
9. Add `LOGIN_REDIRECT_URL`_ to your project's settings.py.  If you're using the suggestion below, set it to ``/distribute/``.
10. Add ``BASE_PATH`` to your project's settings.py, e.g. ``import os.path BASE_PATH = os.path.dirname(__file__)``. In order to create an Android upload folder on the same level as ``MEDIA_ROOT`` this has to be set.
11. Add the `SITE_ID`_ value in your project's settings.py to the primary key of the Site object that represents your site.
12. Login to the Django Admin and add your server's URL to the Site object's domain name (create one if necessary). On the development server this would be ``http://127.0.0.1:8000/``

.. _`SITE_ID`: https://docs.djangoproject.com/en/1.4/ref/settings/#site-id
.. _`django-cleanup`: https://github.com/un1t/django-cleanup
.. _`LOGIN_REDIRECT_URL: https://docs.djangoproject.com/en/1.4/ref/settings/#login-redirect-url

.. code-block:: python
	
	# inside your project's urls.py
	from django.conf.urls import patterns, include, url
	from django.contrib import admin
	admin.autodiscover()

	urlpatterns = patterns('',
		url(r'^admin/', include(admin.site.urls)),
		url(r'^distribute/', include('django_mobile_app_distribution.urls')),
		url(r'^accounts/', include('django_mobile_app_distribution.auth_urls')),
	)

.. code-block:: python

	# Inside your project's settings.py file
	import os.path
	BASE_PATH = os.path.dirname(__file__)


Security considerations
~~~~~~~~~~~~~~~~~~~~~~~

|    By default iOS apps are uploaded to a folder called ``ios_apps`` within your ``MEDIA_ROOT``.
|    This should generally be safe enough as Ad Hoc iOS apps are provisioned to run on a limited number of devices.

|    On Android however a hijacked signed APK file could be redistributed against your client's wishes which is to be avoided at all cost.
|    To this end Android apps are uploaded with a custom instance of ``FileSystemStorage``. By default, Android apps are uploaded to a folder called ``android`` on the same level as ``MEDIA_ROOT``.  The default upload path within the ``android`` folder is ``android_apps``.
|    You can change the default upload and file storage paths with the following directives in your project's settings.py:

* ``MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME``
* ``MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME``
* ``MOBILE_APP_DISTRIBUTION_ANDROID_FILE_STORAGE_PATH``

.. note:: Make sure the ``android/android_apps`` folder is readable and writable by your webserver, but not served by your webserver.

Notify clients of available app downloads by email
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django Mobile App Distribution exposes an Admin Action that allows you to notify your clients once you've uploaded and app.
An email message is generated that contains a link to the download page.
In order for email messaging to work you need to set the following fields in your settings.py module:

* `EMAIL_HOST`_
* `EMAIL_PORT`_
* `EMAIL_HOST_USER`_
* `EMAIL_HOST_PASSWORD`_
* `EMAIL_USE_TLS`_
* `DEFAULT_FROM_EMAIL`_

.. _`EMAIL_HOST`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST
.. _`EMAIL_PORT`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_PORT
.. _`EMAIL_HOST_USER`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST_USER
.. _`EMAIL_HOST_PASSWORD`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST_PASSWORD
.. _`EMAIL_USE_TLS`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_USE_TLS
.. _`DEFAULT_FROM_EMAIL`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-DEFAULT_FROM_EMAIL


Usage
~~~~~

1. Create a Django Admin User object that represents your client and fill in your client's email and language (very bottom).
2. Make sure your clients can't login to the Django Admin Interface by unchecking the ``Staff status`` and ``Superuser status`` fields.
3. Create iOS or Android Apps to your liking.

Android specifics
~~~~~~~~~~~~~~~~~

In case you get a permission denied error when uploading an Android APK, make sure that the ``android/android_apps`` folder on the same level as ``MEDIA_ROOT`` is writable by your webserver.


Export your iOS app for *Over the Air* distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Overriding the login template logo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to place your own logo on the login screen replace the following file with an image of the size 400x200 pixel:

**static/django_mobile_app_distribution/images/logo@2x.png**

