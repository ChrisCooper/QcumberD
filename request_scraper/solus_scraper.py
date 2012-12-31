from solus_session import SolusSession
import course_catalog.models

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
            subject_attrs = {'title' : subject_title,
                          'abbreviation' : subject_abbr}
            subject = course_catalog.models.existing_or_new(course_catalog.models.Subject, **subject_attrs)
            subject.save()
            
            print ("----Parsing subject: " + str(subject))
            
            # Show courses by clicking the dropdown
            s.dropdown_subject(subject_abbr, subject_title)

            # Scrape all the courses
            self._course_scrape(s, subject)
            
            # Close the course dropdown
            s.dropdown_subject(subject_attrs['abbreviation'], subject_attrs['title'])


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
            course_all_info = s.parser().course_attrs()
            course_x_info = course_all_info['extra']

            course_attrs = course_all_info['basic']
            course_attrs['subject'] = subject

            course = course_catalog.models.existing_or_new(course_catalog.models.Course, **course_attrs)
            
            # Extra info
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
            season = course_catalog.models.existing_or_new(course_catalog.models.Season, name=term_data[1])
            season.save()

            # Save the term information
            term_attrs = {
                    'year' : term_data[0],
                    'season' : season
            }
            term = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attrs)
            term.save()
           
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
            self.store_section_components(section, section_all_info['classes'])

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
            section_type = course_catalog.models.existing_or_new(course_catalog.models.SectionType, abbreviation=section_data['type'])
            section_attrs = {
                        'index_in_course' : section_data['index'],
                        'solus_id' : class_num,
                        'type' : section_type,
                        'course' : course,
                        'term' : term}
            
            section = course_catalog.models.existing_or_new(course_catalog.models.Section, **section_attrs)
            section.save()

            # Store the section data
            self.store_section_components(section, section_data['classes'])

    
    def store_section_components(self, section, class_data):
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
