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



def test_request():
    """Return what should be displayed (html or otherwise)"""
    print ("Logging in")
    s = SolusSession(SCRAPER_USERNAME, SCRAPER_PASSWORD)
    print ("Logged in")

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[:3]: #TESTING, only 3

        print ("-Parsing letter: " + letter)
        s.select_alphanum(letter)

        for subject_code, subject_data in s.parser().all_subjects().items()[:2]: #TESTING, only 2
            
            # Store the subject
            subject_attrs = {'title' : subject_data[0],
                          'abbreviation' : subject_code}
            subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **subject_attrs)
            #subject.save()
            
            print ("--Parsing subject: " + str(subject))
            
            s.dropdown_subject(subject_attrs['abbreviation'], subject_attrs['title'])

            for course_code, course_data in s.parser().all_courses().items()[:2]: # TESTING, only 2

                print ("---Parsing course: " + course_code + " - " + course_data[0])

                s.select_course(course_code)

                course_attrs = s.parser().course_attrs()['basic']
                course_attrs['subject'] = subject
    
                course = course_catalog.models.existing_or_new(course_catalog.models.Course, **course_attrs)
                #course.save()

                s.show_sections()

                for term_key, term_data in s.parser().all_terms().items():
                
                    print ("----Parsing term: " + term_data[0] + " " + term_data[1])

                    s.switch_terms(term_data[0], term_data[1])

                    season = course_catalog.models.existing_or_new(course_catalog.models.Season, name=term_data[1])
                    #season.save()

                    term_attributes = {'year' : term_data[0],
                                       'season' : season}
                    term = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attributes)
                    #term.save()
                    
                    s.show_all_sections()

                    for class_num, section_data in s.parser().all_sections().items():

                        print ("-----Parsing section: " + section_data[0] + "-" + section_data[1] + " (" + class_num + ")")
                        
                        section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=section_data[1])
                        section_attributes = {'index_in_course' : section_data[0],
                                    'solus_id' : class_num,
                                    'type' : section_type,
                                    'course' : course,
                                    'term' : term}
                        
                        section = course_catalog.models.existing_or_new(course_catalog.models.Section, **section_attributes)
                        #section.save()

                        s.view_section(class_num)

                        # Section data
                        section_all_info = s.parser().section_attrs()
    
                        s.return_from_section()

                s.return_from_course()

            # Close the course dropdown
            s.dropdown_subject(subject_attrs['abbreviation'], subject_attrs['title'])
                
    return s.latest_text
