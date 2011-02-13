cli2phone
=========
cli2phone uses Google's [Chrome to Phone](http://code.google.com/p/chrometophone/) features to send push messages to your anrdoid handset from the command line. It requires that your android phone is running Android 2.2 or later, and that the [Google Chrome to Phone](https://market.android.com/details?id=com.google.android.apps.chrometophone) application is installed.

cli2phone has currently only been tested on Linux (Ubuntu 10.10).

Authentication
--------------
cli2phone requires authentication with the Google account the phone is registered with, and will prompt with an authentication URL if it has not previously authenticated.

Dependencies
------------
* python 2.6
* [python_oauth2](https://github.com/simplegeo/python-oauth2) 

See requirements.txt for details.

