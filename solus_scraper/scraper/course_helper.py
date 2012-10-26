import re
import course_catalog.models
import section_helper

def drill_single_course(subject, tools):
    s, config = tools.selen, tools.config

    #Gather the title and description to create a new course
    title, number  = scrape_title(tools)
    description = scrape_description(tools)

    attributes = {'title' : title,
                  'number' : number,
                  'description' : description,
                  'subject' : subject}

    course = course_catalog.models.existing_or_new(course_catalog.models.Course, **attributes)

    course.save()

    section_helper.drill_terms_of_sections(course, tools)

            
def scrape_title(tools):
    s = tools.selen

    raw_title = s.get_text("css=span.PALEVEL0SECONDARY").strip()

    m = re.search('^([\S]+)\s+([\S]+)\s+-\s+(.*)$', raw_title)
        
    subject_abbreviation = m.group(1)
    number = m.group(2)
    title = m.group(3)

    return title, number 

def scrape_description(tools):
    s = tools.selen

    description_locator = "xpath=(//span[@class='PSLONGEDITBOX'])[1]"
    if s.is_element_present(description_locator):
        return s.get_text(description_locator).strip()
    return ""