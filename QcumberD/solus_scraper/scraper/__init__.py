from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

from course_catalog.models import Course

import login_helper

class SolusScraper(object):
    """
    This class uses the Selenium Webdriver to navigate SOLUS, and update course info in the Qcumber database.
    """

    def full_scrape(self):
        print("Beginning scrape job...")

        # Create a new instance of the Firefox driver
        self.driver = webdriver.Firefox()
        d = self.driver

        d.implicitly_wait(30)

        login_helper.navigate_to_course_catalog(d)

        d.quit()

    