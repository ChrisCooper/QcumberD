"""
WSGI config for mentoring project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

has_virtualenv = False

try:
	from virtualenv_activate import ACTIVATE_PATH
	has_virtualenv = True
except ImportError as e:
	pass

#Activate the virtual environment
if has_virtualenv:
	try:
	    execfile(ACTIVATE_PATH, dict(__file__=ACTIVATE_PATH))
	except StandardError as e:
	    raise EnvironmentError ('You might have forgotten to create a virtualenv '\
	    	'in "venv", or you might have forgotten to install the dependencies '\
	    	'into it: ' + str(e))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcumber.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
