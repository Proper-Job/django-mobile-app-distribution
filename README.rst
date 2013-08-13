Django Mobile App Distribution
==============================

Django Mobile App Distribution is a Django app that allows you to distribute iPhone, iPad and Android over the air to your clients.

It is made up of 2 components:

* A Django Admin interface that allows you to upload and assign apps to users.
* A mobile optimized, login protected download area where your clients can download apps that were associated with their login credentials.


Notify clients of available app downloads
=========================================

Django Mobile App Distribution exposes an Admin Action that allows you to notify your clients once you've uploaded and app.
An email message is generated that contains a link to the download page.
In order for email messaging to work you need to set the following fields in your settings.py module:

* `EMAIL_HOST`_
* `EMAIL_PORT`_
* `EMAIL_HOST_USER `_
* `EMAIL_HOST_PASSWORD `_
* `EMAIL_USE_TLS `_
* `DEFAULT_FROM_EMAIL`_

.. _`EMAIL_HOST`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST
.. _`EMAIL_PORT`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_PORT
.. _`EMAIL_HOST_USER`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST_USER
.. _`EMAIL_HOST_PASSWORD`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_HOST_PASSWORD
.. _`EMAIL_USE_TLS `: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-EMAIL_USE_TLS
.. _`DEFAULT_FROM_EMAIL`: https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-DEFAULT_FROM_EMAIL