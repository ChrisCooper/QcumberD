# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n

from solus_session import SolusSession
from solus_data import *



class SolusScraper(object):
    """Scrapes data off Solus"""

    def __init__(self, config, user, password):
        self.config = config
        self.user = user
        self.password = password


    def scrape_all(self):
        """
        Starts a full scrape of the SOLUS site, following the constuctor's configuration.
        """

        print ("Scrape job config:")
        for x in self.config._meta.fields:
            print ("--" + str(x.name) + ": " + str(x.value_from_object(self.config)))
        
        print("Beginning scrape job...")
        
        s = SolusSession(self.user, self.password)

        for letter in self.config.letters:

            print ("--Parsing letter: " + letter)
            s.select_alphanum(letter)

            # Scrapes all the subjects
            self._subject_scrape(s)   
     
    def _subject_scrape(self, s):
        """
        Scrapes subject information.
        Session must be on the subject page.
        """
        
        for subject_abbr, subject_title in s.parser().all_subjects() \
                            [self.config.subject_start_idx:self.config.subject_end_idx]:
            
            # Store the subject information
            subject = e_or_n(cc.Subject, title=subject_title, abbreviation=subject_abbr)
            
            print ("----Parsing subject: " + str(subject))
            
            # Show courses by clicking the dropdown
            s.dropdown_subject(subject_abbr, subject_title)

            # Scrape all the courses
            self._course_scrape(s, subject)
            
            # Close the course dropdown
            s.rollup_subject(subject_abbr, subject_title)


    def _course_scrape(self, s, subject):
        """
        Scrapes course information.
        Session must be on the subject page with dropdown extended.
        """

        for course_code, course_name in s.parser().all_courses() \
                            [self.config.course_start_idx:self.config.course_end_idx]:

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

        for term_key, term_year, term_season in s.parser().all_terms():
        
            print ("--------Parsing term: " + term_year + " " + term_season)

            # Switch to the term
            s.switch_terms(term_year, term_season)

            # Save the season information
            season = e_or_n(cc.Season, name=term_season)
            
            # Save the term information
            term = e_or_n(cc.Term, year=term_year, season=season)
           
            # Scrape section data
            if self.config.deep:
                self._sections_deep_scrape(s, subject, course, term)
            else:
                self._sections_shallow_scrape(s, subject, course, term)

    def scrape_section(section):
        """
        Scrapes an individual section.
        Uses deep scraping so enrollment information is updated.
        """
        s = SolusSession(self.user, self.password)

        #Get information
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

        self._section_scrape(s, subject, course, term, section)

        s.return_from_course()

        s.close_session()


    def _section_scrape(self, s, subject, course, term, section):
        """
        Deep scrapes a section.
        Loads the section page to gather extra info.
        Session must be on the course page.
        """
        
        print ("----------Parsing section: " + section.index_in_course + \
                "-" + section.type.abbreviation + " (" + section.solus_id + ")")
 
        # Click the section
        s.view_section(section.solus_id)

        # Store the section component data (multiple per section)
        section_all_info = s.parser().section_attrs()
        store_section_components(section, section_all_info['classes'])
        store_section_extra_info(section, section_all_info['details'], section_all_info['availability'])

        # Back to the course page
        s.return_from_section()

    def _sections_deep_scrape(self, s, subject, course, term):
        """
        Scrapes section information.
        Loads the section page to gather extra info.
        Session must be on the course page.
        """

        # Click the 'View All' button 
        s.show_all_sections()

        for class_num, class_idx, class_type in s.parser().all_sections():

            # Save the section information
            section_type = e_or_n(cc.SectionType, abbreviation=class_type)
            section = e_or_n(cc.Section,
                        index_in_course=class_idx,
                        solus_id=class_num,
                        type=section_type,
                        course=course,
                        term=term)

            self._section_scrape(s, subject, course, term, section)


    
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
            section_type = e_or_n(cc.SectionType, abbreviation=section_data['type'])

            section = e_or_n(cc.Section,
                        index_in_course=section_data['index'],
                        solus_id=class_num,
                        type=section_type,
                        course=course,
                        term=term)

            # Store the section data
            store_section_components(section, section_data['classes'])

    
