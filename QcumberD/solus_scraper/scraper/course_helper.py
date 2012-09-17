import re
import course_catalog.models

def scrape_single_course(subject, tools):
    d, config = tools.driver, tools.config


    import pdb; pdb.set_trace()

    #Gather the title and description to create a new course
    title, number  = scrape_title(tools)
    description = scrape_description(tools)

    search_attributes = {'subject' : subject,
                         'number' : number}

    creation_attributes = {'title' : title,
                  'number' : number,
                  'description' : description,
                  'subject' : subject}

    course = course_catalog.models.existing_or_new(course_catalog.models.Course,
                                                   search_attributes=search_attributes,
                                                   creation_attributes=creation_attributes)

    course.save()

    return


    #Scrape info from course

    try:
        self.scrape_single_course()
                
        self.course.clean()
                
        self.add_course(self.course)
                
        self.merge_course_if_fullyear()
                
    except SolusModels.UselessCourseException as e:
        print "Ignored"
        SolusModels.SolusCourse.num_courses -= 1
            
def scrape_title(tools):
    d = tools.driver

    title_element = d.find_element_by_css_selector("span.PALEVEL0SECONDARY")
    raw_title = title_element.get_attribute("text").strip()

    m = re.search('^([\S]+)\s+([\S]+)\s+-\s+(.*)$', raw_title)
        
    subejct_abbreviation = m.group(1)
    number = m.group(2)
    title = m.group(3)

    return title, number 

def scrape_description(tools):
    d = tools.driver

    if tools.is_element_present(lambda: d.find_elements_by_css_selector("span.PSLONGEDITBOX")[1]):
        description_element = d.find_elements_by_css_selector("span.PSLONGEDITBOX")[1]
        return description_element.get_attribute("text").strip()
    