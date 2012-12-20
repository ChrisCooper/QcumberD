# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

def configure_databases(dict):
    dict['default']['USER'] = 'db_username'
    dict['default']['PASSWORD'] = 'db_password'
    dict['default']['NAME'] = 'db_name'

ADMINS = (
    ('Admin name', 'admin@email.com'),
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'laksjdlaksdjalksdjalksjdlkasjdlkajsd'