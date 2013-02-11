import re
from datetime import datetime

import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n

from solus_parser import SolusParser

class SectionParser(SolusParser):

    view_all_id = 'CLASS_TBL_VW5$fviewall$0'

    sections_table_css_class = 'PABACKGROUNDINVISIBLEWBO'
    sections_table_id = 'CLASS_TBL_VW5$scroll$0'

    def sections_are_offered(self):
        """Determines whether there is a 'View class sections' button on the page"""
        return self.soup.find("a", {'id': 'DERIVED_SAA_CRS_SSR_PB_GO'})

    def terms_offered(self, ):
        """Returns the terms during which the current term is offered"""

        terms = []

        term_dropdown = self.soup.find("select", {'id': 'DERIVED_SAA_CRS_TERM_ALT'})

        for option in term_dropdown.find_all("option"):

            m = re.search('^([^\s]+) (.*)$', option.get_text())

            dropdown_value = option['value']
            year = m.group(1)
            season = m.group(2)
            
            # Make a real season
            season = e_or_n(cc.Season, name=season)
            season.save(was_scraped=True)

            term = e_or_n(cc.Term, year=year, season=season)

            # Store the dropdown value so we can request this term later in scraping
            term.dropdown_value = dropdown_value

            terms.append(term)

        return terms

    def view_all_section_button_exists(self):
        """Returns whether or not there is a "view all sections" button on the page"""
        return self.soup.find('a', {'id': self.view_all_id})

    def current_sections(self, course, term):
        """Returns all sections visible on the current course page"""

        # Get the table of all sections
        sections_table = self.soup.find('table', {'class': self.sections_table_css_class, 'id': self.sections_table_id})

        # Get the links containing e.g. "001-LEC (1843)"
        section_header_links = sections_table.find_all("a", {"class": "PSHYPERLINK", "title": "Class Details"})

        # Get the tables contating all section components for a given section
        section_component_tables = sections_table.find_all('table', {'id': re.compile(r'CLASS_MTGPAT\$scroll\$')})
        
        # Make sure the size of each list matches
        if len(section_header_links) != len(section_component_tables):
            raise Exception("Number of section headers ({0}) doesn't match number of section_component_tables ({1})".format(
                    len(section_header_links), len(section_component_tables)
                )
            )

        sections = []

        # Build a section out of each section header and table
        for header_link, component_table in zip(section_header_links, section_component_tables):
            section = self.build_section(header_link, component_table, course, term)
            section.save(was_scraped=True)
            sections.append(section)

        return sections

    def build_section(self, header_link, component_table, course, term):

        section = self.section_from_header_link(header_link, course, term)
        section.save()

        component_rows = component_table.find_all('tr', {})

        # Remove the header row
        del(component_rows[0])

        for row in component_rows:
            values = row.find_all('span')
            values = [self.clean_HTML(v.get_text()) for v in values]

            room = values[3]

            instructors_str = values[4]

            # start/end dates
            start_date, end_date = self.date_range(values[5])

            instructors = self.instructors_from_string(instructors_str)

            # Timeslot
            all_days_offered = values[0]
            start_time = values[1]
            end_time = values[2]
            timeslots = self.build_timeslots(all_days_offered, start_time, end_time)

            if timeslots is None:
                # If there's no timeslot, we should still create one component with a TBA timeslot
                timeslots = [None]

            attrs = {
                'section': section,
                'room': room,
                'start_date': start_date,
                'end_date': end_date,
            }
    
            #Create a section component for each day
            for timeslot in timeslots:
                attrs['timeslot'] = timeslot
                component = e_or_n(cc.SectionComponent, **attrs)
                component.instructors = instructors
                component.save(was_scraped=True)

        return section

    def date_range(self, date_range_str):
        """Returns two dates parsed out of a date range string"""
        m = re.search('^([\S]+)\s*-\s*([\S]+)$', date_range_str)
        start_date = datetime.strptime(m.group(1), "%Y/%m/%d") if m else None
        end_date = datetime.strptime(m.group(2), "%Y/%m/%d") if m else None

        return start_date, end_date


    def instructors_from_string(self, instructors_str):
        """Returns a list of instructors built out of a comma separated list of instructors"""

        instructors = []

        if instructors_str and instructors_str != "TBA" and instructors_str != "Staff":

            # Split the list on every comma (one between profs, one after last names)
            fragments = re.sub(r'\s+', ' ', instructors_str).split(",")
            fragments = [l.strip() for l in fragments]

            # Associate every pair of fragments as a full name
            for i in range(0, len(fragments), 2):
                last_name = fragments[i]
                other_names = fragments[i+1]
                full_name = u"%s, %s" % (last_name, other_names)

                instructor = e_or_n(cc.Instructor, name=full_name)
                instructor.save(was_scraped=True)
                instructors.append(instructor)

        return instructors

    def build_timeslots(self, all_days, start_time_str, end_time_str):
        """
        Returns a list of all the timeslots present in a combo like 'MoTuWeSaSu'
        """
        if not all_days or all_days == "TBA":
            return None

        start_time = None
        end_time = None

        if start_time_str and start_time_str != "TBA":
            start_time = datetime.strptime(start_time_str, "%I:%M%p")
        if end_time_str and end_time_str != "TBA":
            end_time = datetime.strptime(end_time_str, "%I:%M%p")

        timeslots = []

        #loop through all days, 2 characters at a time
        while len(all_days) > 0:
            day_abbr = all_days[-2:]
            all_days = all_days[:-2]

            weekday =  e_or_n(cc.DayOfWeek, abbreviation=day_abbr)
            weekday.save()

            timeslot_attributes = {'day_of_week' : weekday,
                                   'start_time' : start_time,
                                   'end_time' : end_time}

            timeslot = e_or_n(cc.Timeslot, **timeslot_attributes)
            timeslot.save(was_scraped=True)

            timeslots.append(timeslot)

        return timeslots


    def section_from_header_link(self, header_link, course, term):
        """Builds a section from the information in the header link, as well as the supplied course and term"""
        m = re.search('(\S+)-(\S+)\s+\((\S+)\)', header_link.get_text())

        # Make a section type for the supplied type
        section_type = e_or_n(cc.SectionType, abbreviation=m.group(2))
        section_type.save()

        attrs = {
            'solus_id': m.group(3),
            'index_in_course': m.group(1),
            'type': section_type,
            'course': course,
            'term': term,
        }
        
        # Make a base section from the supplied attributes
        section = e_or_n(cc.Section, **attrs)

        # Store the link action for visiting later in case of a deep scrape
        section.click_action = header_link['id']

        return section

    def add_section_page_attributes(self, section):
        """Adds the information available on the dedicated section page to the provided section"""

        # Tables for Details, enrollment, availibility, description
        info_tables = self.soup.find_all("table", {"class": "PSGROUPBOXWBO"})
        for table in info_tables:
            header = table.find("td", {"class": "PAGROUPBOXLABELLEVEL1"}).get_text()
            
            if header == "Class Availability":

                labels = table.find_all("label", {"class" : "PSEDITBOXLABEL"})
                values = table.find_all("span", {"class" : "PSEDITBOX_DISPONLY"})

                # Make sure the size of each list matches
                if len(labels) != len(values):
                    raise Exception("Number of enrollment labels ({0}) doesn't match number of values ({1})".format(
                            len(labels), len(values)
                        )
                    )

                for label, value in zip(labels, values):

                    # See which entry we are dealing with
                    if label['for'] == 'SSR_CLS_DTL_WRK_ENRL_CAP':
                        section.class_max = int(value.get_text())
                    elif label['for'] == 'SSR_CLS_DTL_WRK_ENRL_TOT':
                        section.class_curr = int(value.get_text())
                        section.enrollment_was_scraped()
                    elif label['for'] == 'SSR_CLS_DTL_WRK_WAIT_CAP':
                        section.wait_max = int(value.get_text())
                    elif label['for'] == 'SSR_CLS_DTL_WRK_WAIT_TOT':
                        section.wait_curr = int(value.get_text())
                    elif label['for'] == 'SSR_CLS_DTL_WRK_AVAILABLE_SEATS':
                        # Available seats
                        pass
                    else:
                        raise Exception('Unexpected label in section page: "{0}"'.format(label['for']))
                        
                section.save(was_scraped=True)

        return 



