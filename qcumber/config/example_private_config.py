# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This file holds settings that are specific to your environment
#
# THIS IS ONLY AN EXAMPLE. Copy this file to private_config.py and
# fill it out with your environment-specific settings
# DO NOT DISTRIBUTE YOUR PERSONAL private_config.py

#Environment config
CURRENT = "dev" #'dev' (development) or 'prod' (production)

#Caching config (only used in production servers)
CACHE_PATH = "/path/to/memcached/socket"

#Database config
def configure_databases(dict):
    dict['default']['USER'] = 'db_username'
    dict['default']['PASSWORD'] = 'db_password'
    dict['default']['NAME'] = 'db_name'

ADMINS = (
    ('Admin name', 'admin@email.com'),
)
MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'laksjdlaksdjalksdjalksjdlkasjdlkajsd'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

#Email config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'username@domain.com'
EMAIL_HOST_PASSWORD = 'password'
SERVER_EMAIL = 'server@qcumber.ca'
SEND_BROKEN_LINK_EMAILS = True
