from solus_session import SolusSession
from solus_data import *

class SolusScraper(object):
    """Scrapes data off Solus"""

    def __init__(self, config, user, password):
        self.config = config
        self.user = user
        self.password = password


    def full_scrape(self):
        """Starts a full scrape of the SOLUS database"""
        
        print ("Logging in")
        s = SolusSession(self.user, self.password)
        print ("Logged in")

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":

            print ("--Parsing letter: " + letter)
            s.select_alphanum(letter)

            # Scrapes all the subjects
            self._subject_scrape(s)
   
     
    def _subject_scrape(self, s):
        """
        Scrapes subject information.
        Session must be on the subject page.
        """
        
        for subject_abbr, subject_title in s.parser().all_subjects().items():
            
            # Store the subject information
            subject = store_subject({
                            'title' : subject_title,
                            'abbreviation' : subject_abbr})
            
            print ("----Parsing subject: " + str(subject))
            
            # Show courses by clicking the dropdown
            s.dropdown_subject(subject_abbr, subject_title)

            # Scrape all the courses
            self._course_scrape(s, subject)
            
            # Close the course dropdown
            s.dropdown_subject(subject_abbr, subject_title)


    def _course_scrape(self, s, subject):
        """
        Scrapes course information.
        Session must be on the subject page with dropdown extended.
        """

        for course_code, course_name in s.parser().all_courses().items():

            print ("------Parsing course: " + course_code + " - " + course_name)

            # Click the course
            s.select_course(course_code)

            # Store the course information
            course = store_course(subject, s.parser().course_attrs())

            # Scrape all term data
            self._terms_scrape(s, subject, course)

            # Back to the subject/course list
            s.return_from_course()
                    

    def _terms_scrape(self, s, subject, course):
        """
        Scrapes term information.
        Session must be on the course page.
        """
            
        # Show the course sections
        s.show_sections()

        for term_key, term_data in s.parser().all_terms().items():
        
            print ("--------Parsing term: " + term_data[0] + " " + term_data[1])

            # Switch to the term
            s.switch_terms(term_data[0], term_data[1])

            # Save the season information
            season = store_season({"name": term_data[1]})
            
            # Save the term information
            term = store_term({
                    'year' : term_data[0],
                    'season' : season})
           
            # Scrape section data
            #self._sections_deep_scrape(s, subject, course, term)
            self._sections_shallow_scrape(s, subject, course, term)


    def _sections_deep_scrape(self, s, subject, course, term):
        """
        Scrapes section information.
        Loads the section page to gather extra info.
        Session must be on the course page.
        """

        # Click the 'View All' button 
        s.show_all_sections()

        for class_num, section_data in s.parser().all_sections().items():

            print ("----------Parsing section (deep): " + section_data[0] + "-" + section_data[1] + " (" + class_num + ")")
            
            # Save the section information
            section_type = store_section_type({"abbreviation": section_data[1]})
            section = store_section({
                        'index_in_course' : section_data[0],
                        'solus_id' : class_num,
                        'type' : section_type,
                        'course' : course,
                        'term' : term})

            # Click the section
            s.view_section(class_num)

            # Store the section component data (multiple per section)
            section_all_info = s.parser().section_attrs()
            store_section_components(section, section_all_info['classes'])

            # Back to the course page
            s.return_from_section()

    
    def _sections_shallow_scrape(self, s, subject, course, term):
        """
        Scrapes section information.
        Gets section information off the course page.
        Session must be on the course page.
        """
        
        # Click the 'View All' button 
        s.show_all_sections()

        print ("----------Parsing all sections (shallow)")
            
        for class_num, section_data in s.parser().course_section_attrs().items():

            # Save the section information
            section_type = store_section_type({"abbreviation": section_data['type']})

            section = store_section({
                        'index_in_course' : section_data['index'],
                        'solus_id' : class_num,
                        'type' : section_type,
                        'course' : course,
                        'term' : term})

            # Store the section data
            store_section_components(section, section_data['classes'])

    
