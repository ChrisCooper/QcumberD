import re
from datetime import datetime
import course_catalog.models

def scrape_single_section(section_pieces, course, term, tools):

    #For debugging
    if course.number == "834":
        import pdb; pdb.set_trace()    

    #Generate a section from the header
    section = section_from_header(section_pieces, course, term)

    #Add all the components to the section
    while  len(section_pieces) > 0 and (not next_row_is_section_header(section_pieces)):
        scrape_single_section_component(section_pieces, section)
  
    
def next_row_is_section_header(piece_array):
    return re.search('^([\S]+)-([\S]+)\s+\((\S+)\)$', piece_array[0])
    
def scrape_single_section_component(section_pieces, section):

    #For creating the section component later
    component_attributes = {'section' : section}

    #Grab Timeslot info
    #Sometimes all_days is e.g. "MoTuWeSaSu"
    all_days = section_pieces.popleft()
    start_time_str = section_pieces.popleft()
    end_time_str = section_pieces.popleft()
    
    #Constant info
    component_attributes['room'] = section_pieces.popleft()

    instructor_name = section_pieces.popleft()
    if instructor_name == "TBA":
        component_attributes['instructor'] = None
    else:
        component_attributes['instructor'] = course_catalog.models.existing_or_new(course_catalog.models.Instructor, name=instructor_name)

    #Date range
    date_range_str = section_pieces.popleft()
    if date_range_str == "TBA":
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
    else:
        #Create a section component for each day
        for timeslot in timeslots:
            component_attributes['timeslot'] = timeslot
            component = course_catalog.models.existing_or_new(course_catalog.models.SectionComponent, **component_attributes)

def split_into_timeslots(all_days, start_time_str, end_time_str):
    """
    Returns a list of all the timeslots present in a combo like 'MoTuWeSaSu'
    """
    if all_days == "TBA":
        return None

    start_time = None
    end_time = None

    if start_time_str != "TBA":
        start_time = datetime.strptime(start_time_str, "%I:%M%p")
    if end_time_str != "TBA":
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


def section_from_header(piece_array, course, term):
    section_info = piece_array.popleft()
    m = re.search('^([\S]+)-([\S]+)\s+\((\S+)\)$', section_info)
    
    section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=m.group(2))

    attributes = {'index_in_course' : m.group(1),
                  'solus_id' : m.group(3),
                  'type' : section_type,
                  'course' : course,
                  'term' : term}

    section = course_catalog.models.existing_or_new(course_catalog.models.Section, **attributes)


    #discard all the other section header entries, since they're useless for now
    items_discarded = 0
    while section_info != "Select":

        section_info = piece_array.popleft()
        items_discarded += 1
        #Make sure we're not tossing everything away...
        if (items_discarded > 4):
            import pdb; pdb.set_trace()
    
    return section

    