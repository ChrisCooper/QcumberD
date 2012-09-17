import re
import course_helper
import course_catalog.models


#All letters
def drill_subjects_for_letter(letter, tools):
    s, config = tools.selen, tools.config

    tools.wait_for_page()

    #open the letter's page
    s.click("id=DERIVED_SSS_BCC_SSR_ALPHANUM_" + letter)
        
    #Generate the first subject dropdown's link name
    link_number = tools.config.starting_subject_index
    link_name_base = "name=DERIVED_SSS_BCC_GROUP_BOX_1$84$$%d"
    link_name = link_name_base % (link_number,)
       
    #All subject dropdowns
    while s.is_element_present(link_name):

        #Create a subject from the info in the dropdown
        subject = subject_from_dropdown(link_name, tools)

        #drop down the subject
        s.click(link_name)
        tools.wait_for_page()

        drill_subject_dropdown(subject, tools)

        #close the subject dropdown
        s.click(link_name)

        #Generate the next subject dropdown's link name
        link_number += 1
        if config.max_subjects_per_letter and link_number >= config.max_subjects_per_letter + config.starting_subject_index:
            break
            
        link_name = link_name_base % (link_number,)

#Store subject title and abbreviation from the subject dropdown text
def subject_from_dropdown(subject_link_name, tools):
    s = tools.selen

    m = re.search("^([^-]*) - (.*)$", s.get_text(subject_link_name).strip())
      
    subject_key = m.group(1)
    subject_title = m.group(2)
            
    attributes = {'title' : subject_title,
                  'abbreviation' : subject_key}

    subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **attributes)

    subject.save()

    return subject

def drill_subject_dropdown(subject, tools):
    s, config = tools.selen, tools.config

    #Generate the first course's link id
    link_number = config.starting_course_index
    link_id_base = "id=CRSE_TITLE$%d"
    link_id = link_id_base % (link_number,)
        
    #All course links
    while s.is_element_present(link_id):

        #Go into the course
        s.click(link_id)

        course_helper.scrape_single_course(subject, tools)
    
        #Back out from course page
        s.click("id=DERIVED_SAA_CRS_RETURN_PB")

        #Generate the next course's link id
        link_number += 1
            
        if config.max_courses_per_subject and link_number >= config.max_courses_per_subject + config.starting_course_index:
            break
            
        link_id = link_id_base % (link_number,) 

