
def configure_databases(dict):
    dict['default']['USER'] = 'db_username'
    dict['default']['PASSWORD'] = 'db_password'
    dict['default']['NAME'] = 'bd_name'

ADMINS = (
    ('Admin name', 'admin@email.com'),
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'laksjdlaksdjalksdjalksjdlkasjdlkajsd'