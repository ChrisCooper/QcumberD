# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re, cgi
import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n


def store_course(subject, course_all_info):
    """Stores a course object"""
            
    course_x_info = course_all_info.get('extra', None)
    
    course_attrs = course_all_info['basic']
    course_attrs['subject'] = subject
    
    course = e_or_n(cc.Course, **course_attrs)
    
    # Extra info
    if course_x_info:
        if 'career' in course_x_info:
            course.career = e_or_n(cc.Career, name=str(course_x_info['career']))
        if 'units' in course_x_info:
            if len(course_x_info['units'].split(".")[1]) > 2:
                raise Exception('Error: assumption about precision or magnitude of credit hours (units) is false: "%s"' % value)
            course.units = float(course_x_info['units'])
        if 'grading_basis' in course_x_info:
            course.grading_basis = e_or_n(cc.GradingBasis, name=str(course_x_info['grading_basis']))
        if 'enrollment_requirement' in course_x_info:
            course.enrollment_reqs = link_requisites(course_x_info['enrollment_requirement'])
        if 'add_consent' in course_x_info:
            course.add_consent = e_or_n(cc.Consent, name=str(course_x_info['add_consent']))
        if 'drop_consent' in course_x_info:
            course.drop_consent = e_or_n(cc.Consent, name=str(course_x_info['drop_consent']))

    course.save()

    return course


def store_section_extra_info(section, section_details, section_availability):
    """stores extra information about a section retrieved from a deep scrape"""

    # Details
    if 'session' in section_details:
        section.session = e_or_n(cc.Session, name=str(section_details['session']))

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
        timeslot = None
        if clss['day_abbr'] and clss['start_time'] and clss['end_time']:

            # Make timeslot
            weekday = e_or_n(cc.DayOfWeek, abbreviation=clss['day_abbr'])
            timeslot_attrs = {
                'day_of_week' : weekday,
                'start_time' : clss['start_time'],
                'end_time' : clss['end_time']
            }
            timeslot = e_or_n(cc.Timeslot, **timeslot_attrs)

        # Make component
        section_comp_attrs = {
            'section' : section,
            'start_date': clss['start_date'],
            'end_date': clss['end_date'],
            'room': clss['room'],
            'timeslot': timeslot,
        }
        component = e_or_n(cc.SectionComponent, **section_comp_attrs)

        # Add instructors
        for i in clss['instructors']:
            instructor = e_or_n(cc.Instructor, name=i)
            component.instructors.add(instructor)

        component.save()

def link_requisites(s):
    """Makes prereqs link to their respective courses"""

    # We need to escape this string because it is displayed raw later on in the view
    s = cgi.escape(s)
    matches = re.finditer("([A-Z]{3,4})\s*(\d{3}[AB]?)", s)

    #Because we are replacing strings as we go, the match indecies will become incorrect along the way
    index_offset = 0

    for match in matches:
        repr = '<a href="/search/?q=%s+%s">%s %s</a>' % (match.group(1), match.group(2), match.group(1), match.group(2))
        s = s[:match.start() + index_offset] + repr + s[match.end() + index_offset :]
        index_offset += len(repr) - len(match.group(0))
 
    return s
