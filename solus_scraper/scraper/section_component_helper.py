# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from datetime import datetime
import course_catalog.models

def compile_sections_from_component_rows(component_rows, course, term, tools):

    #For debugging
    #if course.number == "834":
    #    import pdb; pdb.set_trace()    

    section = None

    for row in component_rows:
        if row_is_section_header(row):
            section = section_from_header(row, course, term)
        else:
            add_component_to_section(row, section)
  
    
def row_is_section_header(piece_array):
    return re.search('^([\S]+)-([\S]+)\s+\((\S+)\)$', piece_array[0])


def section_from_header(piece_array, course, term):
    section_info = piece_array[0]
    m = re.search('^([\S]+)-([\S]+)\s+\((\S+)\)$', section_info)
    
    section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=m.group(2))

    attributes = {'index_in_course' : m.group(1),
                  'solus_id' : m.group(3),
                  'type' : section_type,
                  'course' : course,
                  'term' : term}

    return course_catalog.models.existing_or_new(course_catalog.models.Section, **attributes)


def add_component_to_section(section_pieces, section):

    #For creating the section component later
    component_attributes = {'section' : section}

    #Grab Timeslot info
    #Sometimes all_days is e.g. "MoTuWeSaSu"
    all_days = section_pieces[0]
    start_time_str = section_pieces[1]
    end_time_str = section_pieces[2]
    
    #Room
    component_attributes['room'] = section_pieces[3]

    #Instructors
    #They are comma seperated, with extra whitespace
    #They also have a comma after their last name
    #e.g. Doe, John C 
    instructors_names = section_pieces[4]
    instructors = []
    if instructors_names and instructors_names != "TBA" and instructors_names != "Staff":
        lis = re.sub(r'\s+', ' ', instructors_names).split(",")
        for i in range(0, len(lis), 2):
            last_name = lis[i].strip()
            other_names = lis[i+1].strip()
            name = u"%s, %s" % (last_name, other_names)
            instructor = course_catalog.models.existing_or_new(course_catalog.models.Instructor, name=name)
            instructors.append(instructor)

    #Date range
    date_range_str = section_pieces[5]
    if not date_range_str or date_range_str == "TBA":
        component_attributes['start_date'] = None
        component_attributes['end_date'] = None
    else:
        m = re.search('^([\S]+)\s*-\s*([\S]+)$', date_range_str)

        component_attributes['start_date'] = datetime.strptime(m.group(1), "%Y/%m/%d")
        component_attributes['end_date'] = datetime.strptime(m.group(2), "%Y/%m/%d")
        
    timeslots = split_into_timeslots(all_days, start_time_str, end_time_str)

    if timeslots is None:
        component_attributes['timeslot'] = None
        component = course_catalog.models.existing_or_new(course_catalog.models.SectionComponent, **component_attributes)
        for i in instructors:
            component.instructors.add(i)
        component.save()
    else:
        #Create a section component for each day
        for timeslot in timeslots:
            component_attributes['timeslot'] = timeslot
            component = course_catalog.models.existing_or_new(course_catalog.models.SectionComponent, **component_attributes)
            for i in instructors:
                component.instructors.add(i)
            component.save()

def split_into_timeslots(all_days, start_time_str, end_time_str):
    """
    Returns a list of all the timeslots present in a combo like 'MoTuWeSaSu'
    """
    if not all_days or all_days == "TBA":
        return None

    start_time = None
    end_time = None

    if start_time_str and start_time_str != "TBA":
        start_time = datetime.strptime(start_time_str, "%I:%M%p")
    if end_time_str and end_time_str != "TBA":
        end_time = datetime.strptime(end_time_str, "%I:%M%p")

    timeslots = []

    #loop through all days
    while len(all_days) > 0:
        day_abbr = all_days[-2:]
        all_days = all_days[:-2]

        weekday = course_catalog.models.existing_or_new(course_catalog.models.DayOfWeek, abbreviation=day_abbr)

        timeslot_attributes = {'day_of_week' : weekday,
                               'start_time' : start_time,
                               'end_time' : end_time}

        timeslots.append(course_catalog.models.existing_or_new(course_catalog.models.Timeslot, **timeslot_attributes))

    return timeslots


    