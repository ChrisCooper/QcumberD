from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

from solus_scraper.models import JobConfig
from course_catalog.models import Course

import login_helper

class SolusScraper(object):
    """
    This class uses the Selenium Webdriver to navigate SOLUS, and update course info in the Qcumber database.
    """

    def full_scrape(self, config):

        print("Beginning scrape job...")

        # Create a new instance of the Firefox driver
        self.driver = webdriver.Firefox()
        d = self.driver

        d.implicitly_wait(config.timeout_milliseconds)

        login_helper.navigate_to_course_catalog(d)

        #for letter in config.subject_letters:


        d.quit()

    