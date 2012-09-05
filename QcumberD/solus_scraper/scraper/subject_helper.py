import course_helper

def scrape_subject_dropdown(tools):
    d, config = tools.driver, tools.config

    #Prepare to traverse all links
    link_number = config.starting_course_index
    link_id_base = "CRSE_TITLE$%d"
    link_id = link_id_base % (link_number,)
        

    while tools.is_element_present(lambda: d.find_element_by_id(link_id)):

        #Go into the course
        course_link = d.find_element_by_id(link_id)
        course_link.click()

        course_helper.scrape_single_course(tools)
    
        #Back out from course page
        return_link = d.find_element_by_id("DERIVED_SAA_CRS_RETURN_PB")
        return_link.click()

        #Go to next course
        link_number += 1
            
        if config.max_courses_per_subject and link_number >= config.max_courses_per_subject + config.starting_course_index:
            break
            
        link_id = link_id_base % (link_number,) 