DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'HOST': '',                      # Set to empty string for localhost.
        'PORT': '',                      # Set to empty string for default.
    }
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

from private_config import *

configure_databases(DATABASES)