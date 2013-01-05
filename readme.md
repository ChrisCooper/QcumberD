Qcumber
=======

Qcumber is a course catalog created for Queen's University. The original source code is available under the terms of the Mozilla Public License, v. 2.0, available at http://mozilla.org/MPL/2.0/. Images and other non-code assets are &copy; 2012 Chris Cooper.


How to get it up and running

This guide has been verified for Ubuntu 12.10.

Setting up on mac OSX should be quite similar. It will be verified soon.

<del>Microsoft Windows offers great pains.</del>It works on Windows, but installation there is left as an exercise for the reader.


Prerequisites
-------------

 * Python 2.7
 * Git
   There may be some extra setup steps I'm forgetting.
   GitHub has great documentation.
 * Pip
 * virtualenv
 * A GitHub account (https://github.com/)

The following command should install all the required packages on Ubuntu 12.10:
```bash
sudo apt-get install git python python-pip virtualenv
```
I (Phil) could not get Qcumber to run under Python 3 after spending a whole couple seconds of trying. I have not tested on any version of Python other than 2.7.

The [django project installation documentation](https://docs.djangoproject.com/en/1.4/intro/install/) would be a good starting point for other operating systems.


Style Notes
-----------

Anything in [square brackets] should be replaced with a value specific to you.

For example, if your username is, say, `uniphil`, then a command like
`mkdir [username]` should be written literally as `mkdir uniphil`.

Steps to Get Set Up
-------------------

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
   to run the local project. You can use the same preceeding `source` command.

 * To deactivate the virtual environment: `deactivate`

4. Install Required Packages
----------------------------

Make sure you have activated your virtual environment (see above) before running this command!

 * `pip install -r requirements.txt`


5. Configure Your Setup
-----------------------

 * Clone the sample config file `cp qcumber/config/example_private_config.py qcumber/config/private_config.py`
 * Change the configuration options in qcumber/config/private_config.py to suit your environment. If you are not performing caching, scraping, or sending emails, nothing needs to change in this file for development.


6. Initialize the Database
--------------------------

Make sure your virtualenv is activated!

 * `python manage.py syncdb`
   Create the administrative account and follow the prompts.
 * Migrate the `south` databases: `python manage.py migrate`.

7. Install LESS compiler
------------
* Install Node.js (including the Node Package Manager, `npm`) [Using a package manager](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) or from [nodejs.org](http://nodejs.org/)
* Install the LESS compiler via the Node Package Manger: `sudo npm install -g less`
* You can now compile LESS files like this: `lessc styles.less > styles.css`, but django-compressor automatically compiles the LESS files in this project.

8. Run Time!
------------

 * `python manage.py runserver`
 * Open a browser and go to [http://localhost:8000](http://localhost:8000)

And hopefully it just works!

The database will be empty, so no courses will be present on your setup.

Extra Notes
-----------

How to Scrape Course Data
-------------------------

 * Download Selenium Server from [http://seleniumhq.org/download/](http://seleniumhq.org/download/)
 * Run the server in another terminal by calling `java -jar [filename].jar`
 * Go to [http://localhost:8000/admin/solus_scraper/jobconfig/](http://localhost:8000/admin/solus_scraper/jobconfig/)
 * Click "Add job config".
 * Add a name ("Scrape everything") and a description.
 * Set the subject letters to "ABCDEFGHIJKLMNOPQRSTUVWXYZ" (all of them).
 * Click "Save".
 * Go to [http://localhost:8000/solus_scraper/](http://localhost:8000/solus_scraper/)
 * Click the name of the job you just created. A browser will open and start navigating the site. As it scrapes, the data will become available to the application. You can watch the subjects being added at [http://localhost:8000](http://localhost:8000)!
 * Scraping usually takes anywhere from 8 to 10 hours, so be patient! (We can also probably send you a copy of our sqlite database if you want to get started faster.)

