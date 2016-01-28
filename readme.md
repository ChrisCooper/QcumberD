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

* This guide has been verified for Ubuntu 15.10.


1. Installing the Prerequisites
-------------------------------

### Python and Libraries ###

This project has been tested with Python version 3.5.
* Install GCC by running `apt-get install gcc`
* Install extra libraries needed for compiling modules: `apt-get install libxml2-dev libxslt1-dev`

### LESS Compiler ###

LESS is an extension of CSS that adds support for dynamic behaviours like variables and functions.

* Install Node.js (including the Node Package Manager, `npm`) [using a package manager](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) or from [http://nodejs.org/](http://nodejs.org/)
* Install the LESS compiler via the Node Package Manger: `npm install -g less`


5. Install Required Packages
----------------------------

Make sure you have activated your virtual environment (see above) before running this command!

* `pip install -r requirements.txt`
* If this command reports an error, check the log to see if you have all the dependencies required.


6. Configure Your Setup
-----------------------

* Clone the sample config file `cp qcumber/config/example_private_config.py qcumber/config/private_config.py`


7. Initialize the Database
--------------------------

Make sure your virtualenv is activated!

* `python manage.py migrate`

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


