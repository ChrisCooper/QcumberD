from selenium import selenium
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from solus_scraper.models import JobConfig, section_types, weekdays
import course_catalog.models

import login_helper
import subject_helper

import re

class ScraperTools(object):
    def __init__(self, selen, config):
        self.selen = selen
        self.config = config
    
    def wait_for_page(self):
        self.selen.wait_for_page_to_load(self.config.timeout_milliseconds)

    def wait_then_click(self, identifier):
        """
        Tries to find an element to click, and if it's not present,
        waits with exponential back-off, then tries again 
        """
        wait_time = 0.5

        while not sel.is_element_present(identifier):
            print("Element not present. Waiting %f seconds..." % wait_time)
            time.sleep(wait_time)
            wait_time *= 2
        time.sleep(3)
        sel.click(identifier)



def full_scrape(config):
    print("Updating constant entries...")
    update_constants()

    print("Beginning scrape job...")

    # Create a new instance of Selenium
    s = selenium("localhost", 4444, "*chrome", "https://sso.queensu.ca/amserver/UI/Login")
    s.start()
        
    s.set_timeout(config.timeout_milliseconds)

    #save our useful stuff to pass around
    tools = ScraperTools(s, config)

    #get to a browsable state
    login_helper.navigate_to_course_catalog(tools)

    #Go through the pages for each letter in the course catalogue

    for letter in config.subject_letters:
        subject_helper.drill_subjects_for_letter(letter, tools)

    print("Completed scrape job")

    s.stop()

   
def update_constants():
    for type_abbr in section_types:
        type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=type_abbr)
        type.name = section_types[type_abbr]
        type.save()

    for day_abbr in weekdays:
        day = course_catalog.models.existing_or_new(course_catalog.models.DayOfWeek, abbreviation=day_abbr)
        day.name = weekdays[day_abbr]
        day.save()