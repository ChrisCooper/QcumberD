from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD
from solus_session import SolusSession
import course_catalog.models

def full_scrape(config):
    """Starts a full scrape of the SOLUS database"""
    sessions = []

def scrape_section(config, section):
    """Refreshes the data for a specific section"""
    pass

def scrape_enrollment(config, section):
    """
    Scrapes the enrollment information of a section
    Returns a (capacity, enrolled) tuple
    """
    # Deprecated by scrape_section()

    s = SolusSession(SCRAPER_USERNAME, SCRAPER_PASSWORD)
    term = section.term
    course = section.course
    subject = course.subject
    
    s.select_alphanum(subject.abbreviation[:1])
    s.dropdown_subject(subject.abbreviation, subject.title)
    s.select_course(course.number)
    s.show_sections()
    s.switch_terms(term.year, term.season)
    s.show_all_sections()
    s.view_section(section.solus_id)

    capacity, enrolled = s.parser().enrollment_stats()

    s.return_from_section()
    s.return_from_course()

    s.close_session()
    
    return capacity, enrolled

def section_shallow_scrape(s, subject, course, term):
    """Gets section information off the course page"""

    print ("----------Parsing all sections (shallow)")
        
    for class_num, section_data in s.parser().course_section_attrs().items():

        # Save the section information
        section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=section_data['type'])
        section_attrs = {
                    'index_in_course' : section_data['index'],
                    'solus_id' : class_num,
                    'type' : section_type,
                    'course' : course,
                    'term' : term}
        
        section = course_catalog.models.existing_or_new(course_catalog.models.Section, **section_attrs)
        section.save()

        for clss in section_data['classes']:

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
            

def section_deep_scrape(s, subject, course, term):
    """Loads the section page to gather extra info"""

    for class_num, section_data in s.parser().all_sections().items():

        print ("----------Parsing section (deep): " + section_data[0] + "-" + section_data[1] + " (" + class_num + ")")
        
        # Save the section information
        section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=section_data[1])
        section_attrs = {
                    'index_in_course' : section_data[0],
                    'solus_id' : class_num,
                    'type' : section_type,
                    'course' : course,
                    'term' : term}
        
        section = course_catalog.models.existing_or_new(course_catalog.models.Section, **section_attrs)
        section.save()

        # Click the section
        s.view_section(class_num)

        # Store the section component data (multiple per section)
        section_all_info = s.parser().section_attrs()
        for clss in section_all_info['classes']:

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
                    'start_date': section_all_info['details']['start_date'],
                    'end_date': section_all_info['details']['end_date'],
                    'room': clss['room'],
                    'timeslot': timeslot
                }
                component = course_catalog.models.existing_or_new(course_catalog.models.SectionComponent, **section_comp_attrs)

                # Add instructors
                for i in clss['instructors']:
                    instructor = course_catalog.models.existing_or_new(course_catalog.models.Instructor, name=i)
                    component.instructors.add(instructor)

                component.save()

        s.return_from_section()



def test_request():
    """Return what should be displayed (html or otherwise)"""

    print ("Logging in")
    s = SolusSession(SCRAPER_USERNAME, SCRAPER_PASSWORD)
    print ("Logged in")

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":

        print ("--Parsing letter: " + letter)
        s.select_alphanum(letter)

        for subject_abbr, subject_title in s.parser().all_subjects().items():
            
            # Store the subject information
            subject_attrs = {'title' : subject_title,
                          'abbreviation' : subject_abbr}
            subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **subject_attrs)
            subject.save()
            
            print ("----Parsing subject: " + str(subject))
            
            # Show courses by clicking the dropdown
            s.dropdown_subject(subject_abbr, subject_title)

            for course_code, course_name in s.parser().all_courses().items():

                print ("------Parsing course: " + course_code + " - " + course_name)

                # Click the course
                s.select_course(course_code)

                # Store the course information
                course_all_info = s.parser().course_attrs()
                course_x_info = course_all_info['extra']

                course_attrs = course_all_info['basic']
                course_attrs['subject'] = subject
    
                course = course_catalog.models.existing_or_new(course_catalog.models.Course, **course_attrs)
                
                # Extra info
                if 'career' in course_x_info:
                    career_attrs = {"name": course_x_info['career']}
                    #course.career = course_catalog.models.existing_or_new(course_catalog.models.Career, **career_attrs)
                if 'units' in course_x_info:
                    if len(course_x_info['units'].split(".")[1]) > 2:
                        raise Exception('Error: assumption about precision or magnitude of credit hours (units) is false: "%s"' % value)
                    course.units = float(course_x_info['units'])
                if 'grading_basis' in course_x_info:
                    grading_attrs = {"name": course_x_info['grading_basis']}
                    #course.grading_basis = course_catalog.models.existing_or_new(course_catalog.models.GradingBasis, **grading_attrs)
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

                # Show the course sections
                s.show_sections()

                for term_key, term_data in s.parser().all_terms().items():
                
                    print ("--------Parsing term: " + term_data[0] + " " + term_data[1])

                    # Switch to the term
                    s.switch_terms(term_data[0], term_data[1])

                    # Save the season information
                    season = course_catalog.models.existing_or_new(course_catalog.models.Season, name=term_data[1])
                    season.save()

                    # Save the term information
                    term_attrs = {
                            'year' : term_data[0],
                            'season' : season
                    }
                    term = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attrs)
                    term.save()
                   
                    # Click the 'View All' button 
                    s.show_all_sections()

                    # Scrape section data
                    #section_deep_scrape(s, subject, course, term)
                    section_shallow_scrape(s, subject, course, term)


                s.return_from_course()

            # Close the course dropdown
            s.dropdown_subject(subject_attrs['abbreviation'], subject_attrs['title'])
                
    return s.latest_text
