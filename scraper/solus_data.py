# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import course_catalog.models
from scraper.models import section_types, weekdays


def update_constants():
    """Updates the constant entries"""

    print("Updating constant entries...")

    for type_abbr in section_types:
        type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=type_abbr)
        type.name = section_types[type_abbr]
        type.save()

    for day_abbr in weekdays:
        day = course_catalog.models.existing_or_new(course_catalog.models.DayOfWeek, abbreviation=day_abbr)
        day.name = weekdays[day_abbr]
        day.save()

    print ("Done!")

def store_subject(subject_attrs):
    """Stores a subject object"""
    
    subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **subject_attrs)
    #subject.save()

    return subject


def store_course(subject, course_all_info):
    """Stores a course object"""
            
    course_x_info = course_all_info.get('extra', None)
    
    course_attrs = course_all_info['basic']
    course_attrs['subject'] = subject
    
    course = course_catalog.models.existing_or_new(course_catalog.models.Course, **course_attrs)
    
    # Extra info
    if course_x_info:
        if 'career' in course_x_info:
            course.career = course_catalog.models.existing_or_new(course_catalog.models.Career, name=str(course_x_info['career']))
        if 'units' in course_x_info:
            if len(course_x_info['units'].split(".")[1]) > 2:
                raise Exception('Error: assumption about precision or magnitude of credit hours (units) is false: "%s"' % value)
            course.units = float(course_x_info['units'])
        if 'grading_basis' in course_x_info:
            course.grading_basis = course_catalog.models.existing_or_new(course_catalog.models.GradingBasis, name=str(course_x_info['grading_basis']))
        if 'enrollment_requirement' in course_x_info:
            course.enrollment_reqs = link_requisites(course_x_info['enrollment_requirement'])
        if 'typically_offered' in course_x_info:
            # Where does this info come from?
            # Do we need it?
            #for x in course_x_info['typically_offered'].split(","):
            #    season = store_season({"name": x.strip()})
            #    course.typically_offered.add(season)
            pass
        if 'course_components' in course_x_info:
            pass
        if 'add_consent' in course_x_info:
            course.add_consent = store_consent({"name" : str(course_x_info['add_consent'])})
        if 'drop_consent' in course_x_info:
            course.drop_consent = store_consent({"name" : str(course_x_info['drop_consent'])})

    course.save()

    return course


def store_season(season_attrs):
    """Stores a season object"""
    
    season = course_catalog.models.existing_or_new(course_catalog.models.Season, **season_attrs)
    #season.save()

    return season


def store_term(term_attrs):
    """Stores a term object"""

    term = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attrs)
    #term.save()

    return term


def store_section_type(sect_type_attrs):
    """Stores a section type object"""

    section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, **sect_type_attrs)
    #section_type.save()
    
    return section_type


def store_section(section_attrs):
    """Stores a section object"""

    section = course_catalog.models.existing_or_new(course_catalog.models.Section, **section_attrs)
    #section.save()

    return section

def store_session(session_attrs):
    """Stores a session object"""
    
    session = course_catalog.models.existing_or_new(course_catalog.models.Session, **session_attrs)
    #session.save()

    return session

def store_consent(consent_attrs):
    """Stores an add/drop consent property"""

    consent = course_catalog.models.existing_or_new(course_catalog.models.Consent, **consent_attrs)

    return consent

def store_section_extra_info(section, section_details, section_availability):
    """stores extra information about a section retrieved from a deep scrape"""

    # Details
    if 'session' in section_details:
        section.session = store_session({"name": str(section_details['session'])})

    # Enrollment information
    section.class_curr = section_availability.get('class_curr', -1)
    section.class_max = section_availability.get('class_max', -1)
    section.wait_curr = section_availability.get('wait_curr', -1)
    section.wait_max = section_availability.get('wait_max', -1)

    section.save()

def store_section_components(section, class_data):
    """Stores the section components"""

    for clss in class_data:

        # Only bother if the timeslot is scheduled
        if clss['day_abbr'] and clss['start_time'] and clss['end_time']:

            # Make timeslot
            weekday = course_catalog.models.existing_or_new(course_catalog.models.DayOfWeek, abbreviation=clss['day_abbr'])
            timeslot_attrs = {
                'day_of_week' : weekday,
                'start_time' : clss['start_time'],
                'end_time' : clss['end_time']
            }
            timeslot = course_catalog.models.existing_or_new(course_catalog.models.Timeslot, **timeslot_attrs)

            # Make component
            section_comp_attrs = {
                'section' : section,
                'start_date': clss['start_date'],
                'end_date': clss['end_date'],
                'room': clss['room'],
                'timeslot': timeslot
            }
            component = course_catalog.models.existing_or_new(course_catalog.models.SectionComponent, **section_comp_attrs)

            # Add instructors
            for i in clss['instructors']:
                instructor = course_catalog.models.existing_or_new(course_catalog.models.Instructor, name=i)
                component.instructors.add(instructor)

            component.save()


def link_requisites(s):
    """Makes prereqs link to their respective courses"""

    # BeautifulSoup should've escaped this already
    #s = cgi.escape(s)
    matches = re.finditer("([A-Z]{3,4})\s*(\d{3}[AB]?)", s)

    #Because we are replacing strings as we go, the match indecies will become incorrect along the way
    index_offset = 0

    for match in matches:
        repr = '<a href="/search/?q=%s+%s">%s %s</a>' % (match.group(1), match.group(2), match.group(1), match.group(2))
        s = s[:match.start() + index_offset] + repr + s[match.end() + index_offset :]
        index_offset += len(repr) - len(match.group(0))
 
    return s
