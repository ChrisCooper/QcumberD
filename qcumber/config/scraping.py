# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
