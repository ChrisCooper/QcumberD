from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time

from solus_scraper.models import JobConfig
import course_catalog.models

import login_helper
import subject_helper

import re

class ScraperTools(object):
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    #Since this is not possible with WebDriver
    #make sure to alter and then reset the timeout
    def is_element_present(self, find_lambda):
        self.driver.implicitly_wait(0)
        is_present = True
        try:
            find_lambda()
        except NoSuchElementException:
            is_present = False
        except IndexError:
            is_present = False
        self.driver.implicitly_wait(self.config.timeout_milliseconds)
        return is_present

    def safe_find_element_by_id(self, id):
        """
        Tries to find an element, and if the web driver throws an excpetion,
        waits with exponential back-off, then tries again 
        """
        successful = False
        wait_time = 0.5
        while (not successful) and wait_time * 1000 < self.config.timeout_milliseconds:
            try:
                return self.driver.find_element_by_id(id)
                successful = True
            except WebDriverException:
                import pdb; pdb.set_trace()
                time.sleep(wait_time)
                wait_time *= 2



def full_scrape(config):

    print("Beginning scrape job...")

    # Create a new instance of the web driver
    d = webdriver.Firefox()
    #d = webdriver.Chrome()

    #save our useful stuff to pass around
    tools = ScraperTools(d, config)

    #set the default timeout for find operations
    d.implicitly_wait(config.timeout_milliseconds)

    #get to a browsable state
    login_helper.navigate_to_course_catalog(d)

    #Go through the pages for each letter in the course catalogue

    for letter in config.subject_letters:
        subject_helper.drill_subjects_for_letter(letter, tools)

    print("Completed scrape job")

    d.quit()

   
