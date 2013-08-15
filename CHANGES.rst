Changelog for Django Mobile App Distribution
============================================

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