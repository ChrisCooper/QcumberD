# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# -----------------------------------------------------------------------------
# This file holds settings that are specific to your environment
#
# THIS IS ONLY AN EXAMPLE. Copy this file to private_config.py and
# fill it out with your environment-specific settings
# DO NOT DISTRIBUTE YOUR PERSONAL private_config.py
# -----------------------------------------------------------------------------

from qcumber.config import unixy_project_path


# Turn debug on in dev settings for useful error pages
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SHOW_DEBUG_TOOLBAR = False


# Database config

# Set this to true to access the remote database. NOTE: you must set up an ssh tunnel from local 5433 to remote 5432
REMOTE_SCRAPE = False

DATABASES = {}

if not REMOTE_SCRAPE:

    # Edit this to make changes to your database setup
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': unixy_project_path('dev_db.sqlite3'),   # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:

    # You can use this for convenience to access the remote database through an ssh tunnel
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'qcumber',   # Or path to database file if using sqlite3.
            'USER': 'qcumber_user',                      # Not used with sqlite3.
            'PASSWORD': 'mypassword',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5433',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

# Site scraping config
SCRAPER_USERNAME = 'netid'
SCRAPER_PASSWORD = 'password'



# OPTIONAL SETTINGS -----------------------------------------------------------
# The settings that follow are mostly for production enviroments.
# You probably only need to worry about these if you're testing specific
# functionalities like caching behaviour or the sending of emails
# -----------------------------------------------------------------------------


ADMINS = (
    ('Admin name', 'admin@email.com'),
)
MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'laksjdlaksdjalksdjalksjdlkasjdlkajsd'


# Cache Settings (don't worry about this unless you're testing caching)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'

        # Replace the DummyCache Backend with these lines to enable real caching in prod or cache-testing senarios
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': 'unix:' + '/path/to/your/memcached.sock',
    }
}


# Email config (Don't worry about this unless you plan to send emails from your dev environment)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'username@domain.com'
EMAIL_HOST_PASSWORD = 'password'
SERVER_EMAIL = 'server@qcumber.ca'
SEND_BROKEN_LINK_EMAILS = True

#Social-Auth keys 
TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''
FACEBOOK_APP_ID              = ''
FACEBOOK_API_SECRET          = ''
GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''

