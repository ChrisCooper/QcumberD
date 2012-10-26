DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'HOST': '',                      # Set to empty string for localhost.
        'PORT': '5433',                      # Set to empty string for default.
    }
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

from private_scraping_config import *

configure_databases(DATABASES)
