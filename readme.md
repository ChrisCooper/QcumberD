Qcumber served its purpose well for a number of years but was eventually retired after serving 1.5 million pageviews from a population of 28,000 students. You can read about its life in this [blog post](https://github.com/ChrisCooper/coopernetics/blob/master/_posts/2015-03-26-qcumber-queens-course-catalogue-retrospective.md), or find a partially archived version on [Wayback Machine](https://web.archive.org/web/20160715163549/http://qcumber.ca/catalog/BIOL/243/)

![A course listing on Qcumber](https://github.com/ChrisCooper/coopernetics/blob/master/static/images/posts/qcumber/course-page.png)

Qcumber
=======

Qcumber is a course catalog created for Queen's University students. It is live at http://qcumber.ca, and the main repository is at [ChrisCooper/QcumberD](https://github.com/ChrisCooper/QcumberD) on Github. Check out the [wiki](https://github.com/ChrisCooper/QcumberD/wiki) for extra information not in this readme, or the [about page](http://qcumber.ca/about/) for more information on the project's origins and goals.

The original source code is available under the terms of the Mozilla Public License, v. 2.0, available at http://mozilla.org/MPL/2.0/. Images and other original non-code assets are &copy; 2013 Chris Cooper.

Development overview
===========

Qcumber, for the most part, is composed of [web scrapers](http://en.wikipedia.org/wiki/Web_scraping) which pull data into the database, and simple Django apps that display that data on the website. For example, the exam scraper visits [ExamBank](http://library.queensu.ca/exambank/) and pulls all the exam links into simple database entries, and the corresponding Django app (basically just a directory in the project) contains definitions that help make sense of the database entries (known as models), as well as a few related things. The logic for the website itself is actually very simple. Really, all it does is display that data (though we are adding functionality as we speak).

All general configuration is under the `qcumber` directory, including `settings.py`, the root URL configuration file, javascript + images + CSS ([LESS](http://lesscss.org/), actually), and files for storing private information like keys, file paths, and passwords (which are not committed to the respository).

To get your own copy of Qcumber to develop or improve, first follow the setup directions below, then run the scrapers for the data you wish to see (i.e. currently: courses, exams, and/or textbooks).

Setup Guide
===========

* This guide has been verified for Ubuntu 11.10 and 12.10.
* Setting up on mac OSX should be quite similar. It will be verified soon.
* <del>Microsoft Windows offers great pains.</del>It works on Windows, but installation there is left as an exercise for the reader.


1. Installing the Prerequisites
-------------------------------

* Make sure you have all the needed permissions to install.
* For most users, this means prepending each install command with `sudo`
* Ex: `sudo apt-get install ...`

### Python and Libraries ###

This project has been tested with Python version 2.7. You can try other 2.x versions, but no promises.

* Run `apt-get install python2.7 python2.7-dev`
* This installs Python 2.7 as well as the headers needed for compiling python modules.
* Some modules that will be installed need to be compiled with GCC.
* Install GCC by running `apt-get install gcc`
* Install extra libraries needed for compiling modules: `apt-get install libxml2-dev libxslt1-dev`

I (Phil) could not get Qcumber to run under Python 3 after spending a whole couple seconds of trying. I have not tested on any version of Python other than 2.7.

The [django project installation documentation](https://docs.djangoproject.com/en/1.4/intro/install/) would be a good starting point for other operating systems.


### Git and a Github account ###

* Go to [https://github.com/](https://github.com/) and follow the instructions to register an account.
* Run `apt-get install git` to install Git.
* Follow the guide at [https://help.github.com/articles/set-up-git](https://help.github.com/articles/set-up-git) to set up Git.


### Pip and a Virtual Environment ###

Pip is used to install extra Python modules that aren't included by default.
A virtual environment is an isolated Python environment. It allows for per-program environment configuration.

* Install Pip by running `apt-get install python-pip`
* Once Pip is installed, run `pip install virtualenv`
* The virtual environment will be configured later.

### LESS Compiler ###

LESS is an extension of CSS that adds support for dynamic behaviours like variables and functions.

* Install Node.js (including the Node Package Manager, `npm`) [using a package manager](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) or from [http://nodejs.org/](http://nodejs.org/)
* Install the LESS compiler via the Node Package Manger: `npm install -g less`
* You can now compile LESS files like this: `lessc styles.less > styles.css` (this is automatically done in this project).


2. Fork the Repository
----------------------

* Click the "Fork" button at the top-right of [https://github.com/ChrisCooper/QcumberD](https://github.com/ChrisCooper/QcumberD)
* You now have your own copy of QcumberD that you can safely mess around with!


3. Clone it to your computer
----------------------------

* Copy the `git@github.com:[yourusername]/QcumberD.git` link on the page.
* Open up a terminal window.
* Navigate to the folder in which you want to store your local copy of Qcumber. For me that would mean `cd ~/Code`
* Clone the repository. `git clone [repository]`, where `[repository]` is the `git@github...` url you copied earlier. 
* You should now have a `QcumberD` folder.


4. Create and Activate a Virtual Environment
--------------------------------------------

* Navigate into the `QcumberD` folder: `cd QcumberD`.
* Create a new virtual environment: `virtualenv --distribute venv`
* Activate the new environment: `source venv/bin/activate`

* NOTE: you will need to activate the virtual environment every time you want to run the local project. You can use the same preceeding `source` command.

* To deactivate the virtual environment: `deactivate`


5. Install Required Packages
----------------------------

Make sure you have activated your virtual environment (see above) before running this command!

* `pip install -r requirements.txt`
* If this command reports an error, check the log to see if you have all the dependencies required.


6. Configure Your Setup
-----------------------

* Clone the sample config file `cp qcumber/config/example_private_config.py qcumber/config/private_config.py`
* Change the configuration options in qcumber/config/private_config.py to suit your environment. If you are not performing caching, scraping, or sending emails, nothing needs to change in this file for development.


7. Initialize the Database
--------------------------

Make sure your virtualenv is activated!

* `python manage.py syncdb`
* Create the administrative account and follow the prompts.
* Migrate the `south` databases: `python manage.py migrate`.

8. Run Time!
------------

* `python manage.py runserver`
* Open a browser and go to [http://localhost:8000](http://localhost:8000)
* If everything works, you'll see the Qcumber home page!
* The database will be empty, so no courses will be present on your setup.

Extra Notes
===========

How to Scrape Course Data
-------------------------

* Go to [http://localhost:8000/scraper/](http://localhost:8000/scraper/)
* Click the name of one of the jobs. The page status will show as "Waiting for localhost..." while the scraper works.
* As it scrapes, the progress of the scraper will be visible in your terminal and the retrieved data will become available to the application.
* You can watch the subjects being added at [http://localhost:8000](http://localhost:8000)!
 Scraping time will vary based on the configuration, but a full shallow scrape takes anywhere from 5 to 7 hours, so be patient!

You can also create your own configurations for debugging, by visiting the admin page and creating a `Job Config`, under `scraper`. Job configs have the following options:

  * Deep: If this is set, the scraper will do a deep scrape (takes longer, but collects enrollment information)
  * Letters: The subject letters to scrape
  * Start/end indecies: Controls which subjects/courses to scrape. Implemented with Python list slices.
  * 

libssl Errors
-------------
* On Mac OS, if you are seeing an error like:

>     ImportError: dlopen(/Users/Me/QcumberD/venv/lib/python2.7/site-packages/psycopg2/_psycopg.so, 2): Library not loaded: @loader_path/../lib/libssl.dylib
>     Referenced from: /usr/lib/libpq.5.dylib
>     Reason: Incompatible library version: libpq.5.dylib requires version 1.0.0 or later, but libssl.0.9.8.dylib provides version 0.9.8

 then you may need to look at [this Stack Overflow answer](http://stackoverflow.com/a/11723752) for the simple solution.


