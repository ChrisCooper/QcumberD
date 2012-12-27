Qcumber
=======

Qcumber is a course catalog created for Queen's University. The original source code is available under the terms of the Mozilla Public License, v. 2.0, available at http://mozilla.org/MPL/2.0/. Images and other non-code assets are &copy; 2012 Chris Cooper.


How to get it up and running

This guide has been verified for Ubuntu 12.10.

Setting up on mac OSX should be quite similar. It will be verified soon.

<del>Microsoft Windows offers great pains.</del>It works on Windows, but installation there is left as an exercise for the reader.


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
 * Open up a terminal window.
 * Navigate to the folder in which you want to store your local copy of
   Qcumber. For me that would mean `cd ~/Code`
 * Clone the repository. `git clone [repository]`, where `[repository]` is the
   `git@github...` url you copied earlier. 

   You should now have a `QcumberD` folder.


3. Create and Activate a Virtual Environment
--------------------------------------------

 * Navigate into the `QcumberD` folder: `cd QcumberD`.
 * Create a new virtual environment: `virtualenv --distribute venv`
 * Activate the new environment: `source venv/bin/activate`

   Note: you will need to activate the virtual environment every time you want
   to run the local project. You an use the same preceeding `source` command.

 * To deactivate the virtual environment: `deactivate`

4. Install Required Packages
----------------------------

Make sure you have activated your virtual environment!

 * `pip install -r requirements.txt`


5. Configure Your Setup
-----------------------

 * Clone the sample config file `cp qcumber/config/example_private_config.py qcumber/config/private_config.py`
 * Change the configuration options in qcumber/config/private_config.py to suit your environment.
   * DEP_TYPE: The deployment type ('dev' for development, 'prod' for production).
   * VENV_ACTIVATE: The path to the virtual environment activate script. Default is usually correct.
   * CACHE_PATH: The path to the mamcached socket. Production environment only.
   * Database configuration: The configuration of the database the application will use.
   * Email config: The settings for sending emails. 
   * Site scraping config: Your netid and password to access SOLUS.


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


8. Scrape Course Data
---------------------

 * Download Selenium Server from `http://seleniumhq.org/download/`
 * Run the server in another terminal by calling `java -jar [filename].jar`
 * Configure scraper: `mkdir ignored_files ; echo -e "[netid]\\n[password]" > ignored_files/selenium_config.txt`
 * Go to `http://localhost:8000/admin/solus_scraper/jobconfig/`
 * Click "Add job config".
 * Add a name ("Scrape everything") and a description.
 * Set the subject letters to "ABCDEFGHIJKLMNOPQRSTUVWXYZ" (all of them).
 * Click "Save".
 * Go to `http://localhost:8000/solus_scraper/`
 * Click the name of the job you just created.
 * A browser will open and start navigating the site.
 * As it scrapes, the data will become available in the web interface.
 * Scraping usually takes anywhere from 8 to 10 hours, be patient!
