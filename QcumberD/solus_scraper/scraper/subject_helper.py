import re
import course_helper
import course_catalog.models


#All letters
def drill_subjects_for_letter(letter, tools):
    d = tools.driver

    #open the letter's page
    letter_link = d.find_element_by_id('DERIVED_SSS_BCC_SSR_ALPHANUM_' + letter)
    letter_link.click()
        
    #Generate the first subject dropdown's link name
    link_number = tools.config.starting_subject_index
    link_name_base = "DERIVED_SSS_BCC_GROUP_BOX_1$84$$%d"
    link_name = link_name_base % (link_number,)
       
    #All subject dropdowns
    while tools.is_element_present(lambda: d.find_element_by_name(link_name)):
        
        subject_title_link = tools.driver.find_element_by_name(link_name)

        #Create a subject from the info in the dropdown
        subject = subject_from_dropdown(subject_title_link, tools)

        #drop down the subject
        subject_title_link.click()

        drill_subject_dropdown(subject, tools)

        #close the subject dropdown
        subject_title_link.click()

        #Generate the next subject dropdown's link name
        link_number += 1
        if config.max_subjects_per_letter and link_number >= config.max_subjects_per_letter + config.starting_subject_index:
            break
            
        link_name = link_name_base % (link_number,)

#Store subject title and abbreviation from the subject dropdown text
def subject_from_dropdown(subject_title_link, tools):

    m = re.search("^([^-]*) - (.*)$", subject_title_link.get_attribute("text").strip())
            
    subject_key = m.group(1)
    subject_title = m.group(2)
            
    attributes = {'title' : subject_title,
                  'abbreviation' : subject_key}

    subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **attributes)

    subject.save()

    return subject

def drill_subject_dropdown(subject, tools):
    d, config = tools.driver, tools.config

    #Generate the first course's link id
    link_number = config.starting_course_index
    link_id_base = "CRSE_TITLE$%d"
    link_id = link_id_base % (link_number,)
        
    #All course links
    while tools.is_element_present(lambda: d.find_element_by_id(link_id)):

        #Go into the course
        course_link = d.find_element_by_id(link_id)
        course_link.click()

        course_helper.scrape_single_course(subject, tools)
    
        #Back out from course page
        return_link = tools.safe_find_element_by_id("DERIVED_SAA_CRS_RETURN_PB")
        return_link.click()

        #Generate the next course's link id
        link_number += 1
            
        if config.max_courses_per_subject and link_number >= config.max_courses_per_subject + config.starting_course_index:
            break
            
        link_id = link_id_base % (link_number,) 

