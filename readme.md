Qcumber
=======

Qcumber is a course catalog created for Queen's University. The original source code is available under the terms of the Mozilla Public License, v. 2.0, available at http://mozilla.org/MPL/2.0/. Images and other non-code assets are &copy; 2012 Chris Cooper.


How to get it up and running

This guide has been verified for Ubuntu 12.10.

Setting up on mac OSX should be quite similar. It will be verified soon.

<del>Microsoft Windows offers great pains.</del>It works on Windows, but installation there is left as an exercise for the reader.


Prerequisites
-------------

 * Python (`apt-get install python`)
 * Git (`apt-get install git`)
   There may be some extra setup steps I'm forgetting.
   GitHub has great documentation.
 * lxml (`apt-get install python-lxml`)
 * Pip (`apt-get install python-pip`)
 * virtualenv (`pip install virtualenv`)
 * A GitHub account (https://github.com/)


Style Notes
-----------

Anything in [square brackets] should be replaced with a value specific to you.

For example, if your username is, say, `uniphil`, then a command like
`mkdir [username]` would be written literally as `mkdir uniphil`.

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
* Install Node.js (including the Node Package Manager, `npm`) [Using a package manager](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) or from [http://nodejs.org/](http://nodejs.org/)
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

 * Go to [http://localhost:8000/admin/scraper/jobconfig/](http://localhost:8000/admin/scraper/jobconfig/)
 * Click "Add job config".
 * Add a name and a description of your scrape job.
 * There are a few options on this page (the default shallow-scrapes everything):
   * Deep: If this is set, the scraper will do a deep scrape (takes longer, pulls additional information)
   * Letters: The subject letters to scrape
   * Start/end indecies: Controls which subjects/courses to scrape. Implemented with Python list slices.
 * For a very minimal scrape (only 1 course per letter), set both the start indecies to 0 and both the end indecies to 0.
 * Click "Save".
 * Go to [http://localhost:8000/scraper/](http://localhost:8000/scraper/)
 * Click the name of the job you just created. The page status will show as "Waiting for localhost..." while the scraper works.
 * As it scrapes, the progress of the scraper will be visible in your terminal and the retrieved data will become available to the application.
 * You can watch the subjects being added at [http://localhost:8000](http://localhost:8000)!
 * Scraping time will vary based on the configuration, but a full shallow scrape takes anywhere from 5 to 7 hours, so be patient!
