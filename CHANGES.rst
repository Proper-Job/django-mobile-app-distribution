Changelog for Django Mobile App Distribution
============================================

0.3.11 (2016-01-18)
----------------

- Fixed migrations being created when app is deployed.

s
0.3.10 (2015-09-21)
----------------

- Fixed packaging


0.3.9 (2015-09-21)
----------------

- Fixed admin model forms ImproperlyConfigured exception.


0.3.8 (2015-09-10)
----------------

- Fix plist syntax error in iOS 9 style manifest.plist.


0.3.7 (2015-08-07)
----------------

- Added support for iOS 9 style manifest.plist configuration.
- Dropped support for Django < 1.7, use 0.3.6 for that.


0.3.6 (2015-07-30)
----------------

- Added Python 3 and Django 1.8 support.


0.3.5 (2015-04-29)
----------------

- Removed logo from login and logout templates.  Removed header from app_list template.


0.3.4 (2015-04-29)
----------------

- Added way to customize default color scheme.


0.3.3 (2015-04-28)
----------------

- Added Zurb Foundation CSS framework and modernized login, logout and app_list templates.


0.3.1 (2015-04-28)
----------------

- Added support for Django >= 1.7 style migrations.


0.3 (2014-11-18)
----------------

- Version 0.3 is not backwards compatible since Xcode 6 has changed the ad hoc process considerably.  You'll have to delete and re-add all iOS apps.
- Fixed deployment to iOS 8 clients. See https://buildozer.io/ios8 for more details.
- Plist file is now automatically generated for iOS apps since Xcode 6 no longer provides it.
- Fixed group distribution for Android apps



0.2 (2014-03-27)
------------------

- Added South dependency to facilitate schmema migration. Checkout README for instructions to upgrade from version 0.1.x to version 0.2.
- Added the ability to associate apps with user groups.  This makes it possible to make a single app available to a group of users.
- Added search fields to the app admin change lists.


0.1.3 (2014-03-19)
------------------

- Using ugettext_lazy instead of ugettext in models.py, which is noticeable if you have a dynamic language switcher in the admin interface.


0.1.2 (2013-08-15)
------------------

- Django Mobile App Distribution no longer registers a custom User object class, in case other apps already do that.  
	* As a consequence the UserInfo attributes cannot be changed from the User changeform any longer. Instead the UserInfo object can be edited standalone.
- User specific language preferences are now respected in the frontend HTML and email messages.
- Fixes in README


0.1.1 (2013-08-13)
------------------

- Fixed template url reverse on Django 1.5 - by using {% load url from future %} in templates

0.1.0 (2013-08-12)
------------------

- Initial release