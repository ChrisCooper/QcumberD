import re

import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n

from solus_parser import SolusParser

class CourseParser(SolusParser):

    title_css_class = 'PALEVEL0SECONDARY'

    info_table_css_class = 'SSSGROUPBOXLTBLUEWBO'
    info_box_css_class = 'PSGROUPBOXNBO'
    info_box_header_css_class = 'SSSGROUPBOXLTBLUE'

    description_css_class = 'PSLONGEDITBOX'

    # The programmatic names for course attributes
    attribute_mappings = {
        "Career": "career",
        "Typically Offered": "typically_offered",
        "Units": "units",
        "Grading Basis": "grading_basis",
        "Add Consent": "add_consent",
        "Drop Consent": "drop_consent",
        "Course Components": "components",
        "Enrollment Requirement": "enrollment_requirement",
    }

    # What model class each attribute should be initialized as
    # (Assume 'str' if not listed)
    attribute_class_mappings = {
        "Career": cc.Career,
        "Grading Basis": cc.GradingBasis,
        "Add Consent": cc.Consent,
        "Drop Consent": cc.Consent,
    }

    def current_course(self, subject):
        """Returns the course built from the current page"""

        # Gather the title and description to create a new course
        title, number  = self.get_title()

        attributes = {'title' : title,
                      'number' : number,
                      'subject' : subject}

        course = e_or_n(cc.Course, **attributes)

        print ("------ Parsing course: {0} - {1}".format(course.number, course.title.encode('ascii','ignore')))

        self.add_info_table_attributes(course)

        return course

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

    def add_info_table_attributes(self, course):
        """Parses the course attributes out of the page and adds them to the supplied course model"""

        # Get the main blue course table containing info boxes such as
        # "Course Detail", "Enrollment Information", and "Description"
        info_table = self.soup.find("table", {"class": self.info_table_css_class})


        # Get each of the boxes within the info table
        info_boxes = self.soup.find_all("table", {"class": self.info_box_css_class})

        for info_box in info_boxes:
            self.add_info_box_attributes(info_box, course)

    def add_info_box_attributes(self, info_box, course):
        """Parses a single box from the info table, and adds the relevant attributes to the course"""

        box_title = info_box.find("td", { "class" : self.info_box_header_css_class})

        if not box_title:
            raise Exception('Encountered unexpected info_box with no title')

        box_title = self.clean_HTML(box_title.get_text())

        if box_title == "Description":
            self.add_description(info_box, course)

        elif box_title in ["Course Detail", "Enrollment Information"]:
            self.add_info_box_content(info_box, course)

        else:
            raise Exception('Encountered unexpected info_box with title: "{0}"'.format(box_title))

        
    def add_description(self, info_box, course):
        description = self.soup.find("span", { "class" : self.description_css_class})
        course.description = self.clean_HTML(description.get_text())


    def add_info_box_content(self, info_box, course):
        """Adds the contents of an info box to the specified course"""

        # Fetch labels and values for "Add/Drop Consent", "Career", and "Grading Basis"
        labels = info_box.find_all("label", {"class":"PSDROPDOWNLABEL"})
        values = info_box.find_all("span", {"class":"PSDROPDOWNLIST_DISPONLY"})

        # Add labels and values for "Typically Offered", "Enrollment Requirement", "Units", and "Course Components"
        labels += info_box.find_all("label", {"class":"PSEDITBOXLABEL"})
        values += info_box.find_all("span", {"class":"PSEDITBOX_DISPONLY"})


        # Extract the "course components" items by checking their parents for a particular table...
        course_components = filter(lambda v: (v.find_parent("table", {'id': 'ACE_width', 'class': 'PABACKGROUNDINVISIBLE'}) is not None), values)
        self.add_course_components(course_components, course)

        # Filter out the course component values from above
        values = filter(lambda v: (v.find_parent("table", {'id': 'ACE_width', 'class': 'PABACKGROUNDINVISIBLE'}) is None), values)

        # Clean the labels and values
        labels = [self.clean_HTML(label.get_text()) for label in labels]
        values = [self.clean_HTML(value.get_text()) for value in values]

        # Filter out the course components label
        if "Course Components" in labels:
            labels.remove("Course Components")

        # Add each of the relevant values to the course
        for label, value in zip(labels, values):
            self.add_attribute_pair(label, value, course)

    def add_attribute_pair(self, attr, value, course):
        """
        Recieves and attribute name and value, and adds it to the course,
        converting it to a model instance first if necessary
        """
        if attr in self.attribute_mappings:
            attribute_name = self.attribute_mappings[attr]

            # Check if we need to make an actual model
            if attr in self.attribute_class_mappings:
                cls = self.attribute_class_mappings[attr]
                value = e_or_n(cls, name=value)

            # Add the attribute's value to the course
            setattr(course, attribute_name, value)

        else:
            raise Exception('Encountered unexpected course attribute with label: "{0}"'.format(label))


    def add_course_components(self, course_components, course):

        components = {}

        # Each pair of values is a key->value pair, so hop by 2
        for i in range(0, len(course_components), 2):
            key = self.clean_HTML(course_components[i].get_text())
            inner_val = self.clean_HTML(course_components[i+1].get_text())
            components[key] = inner_val

        course.components = components

