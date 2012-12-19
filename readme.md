Qcumber
=======

How to get up and running

This guide has been verified for Ubuntu 12.10.

Setting up on mac OSX should be quite similar. It will be verified soon.

<del>Microsoft Windows offers great pains.</del>


Prerequisites
-------------

 * Python (`sudo apt-get install python`)
 * Git (`sudo apt-get install git`)
   There may be some extra setup steps I'm forgetting.
   GitHub has great documentation.
 * Pip (`sudo apt-get install python-pip`)
 * virtualenv (`sudo pip install virtualenv`)
 * A GitHub account (https://github.com/)


Style Notes
-----------

Anything in [square brackets] should be replaced with a value specific to you.

For example, if your username is, say, `uniphil`, then a command like
`mkdir [username]` would be written literally as `mkdir uniphil`.


1. Fork the Repository
----------------------

 * Click the "Fork" button at the top-right on this page:
   https://github.com/ChrisCooper/QcumberD
 * You now have your own copy of QcumberD that you can safely mess around with!


2. Clone it to your computer
----------------------------

 * Copy the `git@github.com:[yourusername]/QcumberD.git` link on the page.
 * Open up terminal (try `ctrl + alt + 'T'`)
 * Navigate to the folder in which you want to store your local copy of
   Qcumber. For me that would mean `cd ~/Code`
 * Clone the repository. `git clone [repository]`, where `[repository]` is the
   `git@github...` url you copied earlier. Note that you can paste into a
   terminal with `ctrl + shift + 'V'` on linux, while the usual `cmd + 'V'`
   works on the mac terminal.

   You should now have a `QcumberD` folder.


3. Create and Activate a Virtual Environment
--------------------------------------------

 * Navigate into the `QcumberD` folder: `cd QcumberD`.
 * Create a new virtual environment: `virtualenv --distribute venv`
 * Activate the new environment: `source venv/bin/activate`

   Note: you will need to activate the virtual environment every time you want
   to run the local project. You an use the same preceeding `source` command.

 * Set up the activation module: `echo "VIRTUALENV_ACTIVATE = 'venv/bin/activate_this.py'" > virtualenv_activate.py`


4. Install Required Packages
----------------------------

Make sure you have activated your virtual environment!

 * `pip install -r requirements.txt`


5. Configure Your Setup
-----------------------

 * current: `cp qcumber/config/example_current.py qcumber/config/current.py`
 * email: `cp qcumber/config/example_email_config.py qcumber/config/email_config.py`
 * private: `cp qcumber/config/example_private_config.py qcumber/config/private_config.py`
 * Edit `db_name` and add a `DATABASES` dict to private_config.py so that it
   looks like this:

```python
def configure_databases(dict):
    dict['default']['USER'] = 'db_username'
    dict['default']['PASSWORD'] = 'db_password'
    dict['default']['NAME'] = 'dev_db.sqlite3'

ADMINS = (
    ('Admin name', 'admin@email.com'),
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'laksjdlaksdjalksdjalksjdlkasjdlkajsd'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
```


6. Initialize the Database
--------------------------

Make sure your virtualenv is activated!

 * `python manage.py syncdb`
   Create the administrative account and follow the prompts.
 * Migrate the `south` databases: `python manage.py migrate`.


7. Run Time!
------------

 * `python manage.py runserver`
 * Open a browser and go to `http://localhost:8000`

And hopefully it just works!

The database will be empty, so no courses are present on your development
setup.

