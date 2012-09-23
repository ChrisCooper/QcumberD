import re
from datetime import datetime
import course_catalog.models

def scrape_single_section(section_pieces, course, term, tools):

    #Generate a section from the header
    section = section_from_header(section_pieces, course, term)
    section.save()

    #Add all the components to the section
    while not next_row_is_section_header(section_pieces) and len(section_pieces) > 0:
        scrape_single_section_component(section_pieces, section)
  
    
def next_row_is_section_header(piece_array):
    if len(piece_array) < 2:
        return False
    if piece_array[-1] == "Select":
        return True
        
    for i in range (-1, -6, -1):
        if re.search('^([\S]+)-([\S]+)\s+\((\S+)\)$', piece_array[i]):
            return True
        
    return False
    
def scrape_single_section_component(section_pieces, section):
    if len(section_pieces) < 6:
        pass#import pdb; pdb.set_trace()

    component_attributes = {}

    #Date range
    m = re.search('^([\S]+)\s*-\s*([\S]+)$', section_pieces.pop())

    component_attributes['start_date'] = datetime.strptime(m.group(1), "%Y/%m/%d")
    component_attributes['end_date'] = datetime.strptime(m.group(2), "%Y/%m/%d")

    instructor_name = section_pieces.pop()
    component_attributes['instructor'] = course_catalog.models.existing_or_new(course_catalog.models.Instructor, name=instructor_name)
    component_attributes['room'] = section_pieces.pop()
        
    #Timeslot
    end_str = section_pieces.pop()
    start_str = section_pieces.pop()
    end_time = datetime.strptime(end_str, "%I:%M%p")
    start_time = datetime.strptime(section_pieces.pop(), "%I:%M%p")
    #Sometimes day is e.g. "MoTuWeSaSu"
    all_days = section_pieces.pop()

        
    #Chop off the days 2 letters at a time to generate all components
    while len(all_days) > 0:
        day_abbr = all_days[-2:]
        all_days = all_days[:-2]

        weekday = course_catalog.models.existing_or_new(course_catalog.models.DayOfWeek, abbreviation=day_abbr)

        timeslot_attributes = {'day_of_week' : weekday,
                               'start_time' : start_time,
                               'end_time' : end_time}

        component_attributes['timeslot'] = course_catalog.models.existing_or_new(course_catalog.models.Timeslot, **timeslot_attributes)

        component_attributes['section'] = section

        component = course_catalog.models.existing_or_new(course_catalog.models.SectionComponent, **component_attributes)

    
def section_from_header(piece_array, course, term):
    section_info = piece_array.pop()
    m = re.search('^([\S]+)-([\S]+)\s+\((\S+)\)$', section_info)
        
    while not m:
        section_info = piece_array.pop()
        m = re.search('^([\S]+)-([\S]+)\s+\((\S+)\)$', section_info)
    
    section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=m.group(2))
    section_type.save()

    attributes = {'index_in_course' : m.group(1),
                  'solus_id' : m.group(3),
                  'type' : section_type,
                  'course' : course,
                  'term' : term}

    return course_catalog.models.existing_or_new(course_catalog.models.Section, **attributes)
    