from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
        self.driver.implicitly_wait(self.config.timeout_milliseconds)
        return is_present



def full_scrape(config):

    print("Beginning scrape job...")

    # Create a new instance of the web driver
    #d = webdriver.Firefox()
    d = webdriver.Chrome()

    #save our useful stuff to pass around
    tools = ScraperTools(d, config)

    #set the default timeout for find operations
    d.implicitly_wait(config.timeout_milliseconds)

    #get to a browsable state
    login_helper.navigate_to_course_catalog(d)

    #Go through all the course catalogue letter and number pages
    for letter in config.subject_letters:
        scrape_subjects_for_letter(letter, tools)

    d.quit()

    
def scrape_subjects_for_letter(letter, tools):
    d = tools.driver

    letter_link = d.find_element_by_id('DERIVED_SSS_BCC_SSR_ALPHANUM_' + letter)
    letter_link.click()
        
    #Prepare to traverse all links
    link_number = tools.config.starting_subject_index
    link_name_base = "DERIVED_SSS_BCC_GROUP_BOX_1$84$$%d"
    link_name = link_name_base % (link_number,)
        
    while tools.is_element_present(lambda: d.find_element_by_name(link_name)):
            
        #Store subject title
        subject_title_link = d.find_element_by_name(link_name)

        m = re.search("^([^-]*) - (.*)$", subject_title_link.get_attribute("text").strip())
            
        subject_key = m.group(1)
        subject_title = m.group(2)
            
        attributes = {'title' : subject_title,
                        'abbreviation' : subject_key}

        subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **attributes)

        subject.save()

        #drop down the subject
        subject_title_link.click()

        subject_helper.scrape_subject_dropdown(tools)

        #close the subject dropdown
        subject_title_link.click()


        #Go to next link
        link_number += 1
        if config.max_subjects_per_letter and link_number >= config.max_subjects_per_letter + config.starting_subject_index:
            break
            
        link_name = link_name_base % (link_number,)
