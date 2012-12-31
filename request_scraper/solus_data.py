import course_catalog.models

def store_subject(subject_attrs):
    """Stores a subject object"""
    
    subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **subject_attrs)
    subject.save()

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
            #course.career = course_catalog.models.existing_or_new(course_catalog.models.Career, name=course_x_info['career'])
            pass
        if 'units' in course_x_info:
            if len(course_x_info['units'].split(".")[1]) > 2:
                raise Exception('Error: assumption about precision or magnitude of credit hours (units) is false: "%s"' % value)
            course.units = float(course_x_info['units'])
        if 'grading_basis' in course_x_info:
            #course.grading_basis = course_catalog.models.existing_or_new(course_catalog.models.GradingBasis, name=course_x_info['grading_basis'])
            pass
        if 'enrollment_requirement' in course_x_info:
            pass #TODO
        if 'typically_offered' in course_x_info:
            pass #TODO
        if 'course_components' in course_x_info:
            pass #TODO
        if 'add_consent' in course_x_info:
            pass #TODO
        if 'drop_consent' in course_x_info:
            pass #TODO
    
    course.save()

    return course


def store_season(season_attrs):
    """Stores a season object"""
    
    season = course_catalog.models.existing_or_new(course_catalog.models.Season, **season_attrs)
    season.save()

    return season


def store_term(term_attrs):
    """Stores a term object"""

    term = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attrs)
    term.save()

    return term


def store_section_type(sect_type_attrs):
    """Stores a section type object"""

    section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, **sect_type_attrs)
    #section_type.save()
    
    return section_type


def store_section(section_attrs):
    """Stores a section object"""

    section = course_catalog.models.existing_or_new(course_catalog.models.Section, **section_attrs)
    section.save()

    return section


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
