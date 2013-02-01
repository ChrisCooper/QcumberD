import re

import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n

from solus_parser import SolusParser

class CourseParser(SolusParser):

    title_css_class = 'PALEVEL0SECONDARY'
    description_css_class = 'PSLONGEDITBOX'

    def current_course(self, subject):
        """Returns the course built from the current page"""

        # Gather the title and description to create a new course
        title, number  = self.get_title()

        print ("------ Parsing course: {0} - {1}".format(number, title))

        import pdb; pdb.set_trace()

        description = self.get_description()


        attributes = {'title' : title,
                      'number' : number,
                      'description' : description,
                      'subject' : subject}

        course = e_or_n(cc.Course, **attributes)

        return

    def get_title(self):

        raw_title = self.soup.find("span", { "class" : self.title_css_class})

        if not raw_title:
            raise Exception("Could not find the course title to parse")

        raw_title = self.clean_HTML(raw_title.get_text())

        m = re.search('^([\S]+)\s+([\S]+)\s+-\s+(.*)$', raw_title)
            
        subject_abbreviation = m.group(1)
        number = m.group(2)
        title = m.group(3)

        return title, number 

    def get_description(self):
        
        description = self.soup.find("span", { "class" : self.description_css_class})

        if description:
            return self.clean_HTML(description.get_text())
        return ""
