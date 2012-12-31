import re
from datetime import datetime
from bs4 import BeautifulSoup

class SolusParser(object):
    """Parses Solus's crappy HTML"""

    def __init__(self, text):
        """Initilizes an instance of BeautifulSoup"""
        # Using lxml, the internal parser fails using Python 2.7.2
        self.soup = BeautifulSoup(text, "lxml")

    #######
    # Get data for POST requests (for a known object)
    #######

    def subject_dropdown(self, abbr, title):
        """Returns the id of the subject dropdown link"""
        return self.soup.find("a", title="Show/Hide Courses for Subject", text="%s - %s" % (abbr, title))['id']

    def course_link(self, number):
        """Returns the id of the course link in the subject dropdown"""
        return self.soup.find("a", { "class": "PSHYPERLINK"}, text=re.compile("%s" % number))['id']

    def section_link(self, class_num):
        """Returns the id of the link to the section on the course page"""
        return self.soup.find("a", { "class": "PSHYPERLINK"}, title="Class Details", text=re.compile("\(%s\)" % class_num))['id']

    def term_key(self, year, season):
        """Returns the key of the term from the term select combobox"""
        return self.soup.find("option", text="%s %s" % (year, season))['value']

    #######
    # Get data for all object POSTs (subject, course, etc)
    #######

    def all_subjects(self):
        """
        Returns a dict of subject data in the current letter
        Format = {abbreviation: title}
        """
        ret = {}
        for tags in self.soup.find_all("a", title="Show/Hide Courses for Subject"):
            abbr, sbj = tags.string.split(" - ")
            ret[abbr] = sbj
        return ret

    def all_courses(self):
        """
        Returns a dict of course data in the expanded subject(s)
        Format = {number: name}
        """
        ret = {}
        for x in self.soup.find_all("a", { "class": "PSHYPERLINK"}):
            # Get a number, then the title
            if "CRSE_TITLE" in x['id']:
                # There are somtimes tags inside the titles
                ret[temp] = "".join([i for i in x.stripped_strings]).strip()
            elif "CRSE_NBR" in x['id']:
                temp = x.string.strip()
        return ret

    def all_terms(self):
        """
        Returns a dict containing term data in the current course
        Format = {key: (year, season)}
        """
        ret = {}
        term_sel = self.soup.find("select", id="DERIVED_SAA_CRS_TERM_ALT")

        # Check if class is scheduled        
        if term_sel:
            for x in term_sel.find_all("option"):
                m = re.search('^([^\s]+) (.*)$', x.string)
                ret[x['value']] = (m.group(1), m.group(2))

        return ret
        
    def all_sections(self):
        """
        Returns a dict containing data for sections in the current term
        Format = {class number: (index, type)}
        """
        ret = {}
        for x in self.soup.find_all("a", {"class": "PSHYPERLINK", "title": "Class Details"}):
            m = re.search('(\S+)-(\S+)\s+\((\S+)\)', x.string)
            ret[m.group(3)] = (m.group(1), m.group(2))
        return ret

    #######
    # Get information
    #######

    def course_section_attrs(self):
        """
        Parses out the section data from the course page.
        Used for shallow scrapes.
        """
        attrs = {
            #class_num :
                #{
                #   'index': 001/002, etc.
                #   'type': LAB/LEC, etc.
                #   'classes': [{
                #       'day_abbr': Mo/Tu/We, etc,
                #       'start_time':datetime object,
                #       'end_time': datetime object,
                #       'room': room,
                #       'instructors': [instructor names],
                #       'start_date': datetime object,
                #       'end_date': datetime object
                #   }]
                #}
            #}
        }

        # Go through all availible sections
        for class_num, section_data in self.all_sections().items():

            # Get the data table for the current course number
            data_table = self.soup.find("table", id="CLASS_MTGPAT$scroll$" + self.section_link(class_num).split("$")[-1])

            # Get the needed cells
            cells = data_table.find_all("span", {"class": "PSEDITBOX_DISPONLY"})
            inst_cells = data_table.find_all("span", {"class": "PSLONGEDITBOX"})
            
            # Iterate over all the classes
            classes = []
            for x in range(0, len(cells), 5):

                # Instructors
                temp_inst = inst_cells[x//5].string
                instructors = []
                if temp_inst and temp_inst != "TBA" and temp_inst  != "Staff":
                    lis = re.sub(r'\s+', ' ', temp_inst).split(",")
                    for i in range(0, len(lis), 2):
                        last_name = lis[i].strip()
                        other_names = lis[i+1].strip()
                        instructors.append(u"%s, %s" % (last_name, other_names))
               
                # Room 
                room = cells[x+3].string
     
                # Class start/end times
                ms = re.search("(\d+:\d+[AP]M)", cells[x+1].string)
                me = re.search("(\d+:\d+[AP]M)", cells[x+2].string)
                start_time = datetime.strptime(ms.group(1), "%I:%M%p") if ms else None
                end_time = datetime.strptime(me.group(1), "%I:%M%p") if me else None

                # Class start/end dates
                m = re.search('^([\S]+)\s*-\s*([\S]+)$', cells[x+4].string)
                start_date = datetime.strptime(m.group(1), "%Y/%m/%d") if m else None
                end_date = datetime.strptime(m.group(2), "%Y/%m/%d") if m else None

                # Loop through all days
                all_days = cells[x+0].string
                while len(all_days) > 0:
                    day_abbr = all_days[-2:]
                    all_days = all_days[:-2]

                    classes.append({
                                'day_abbr': day_abbr,
                                'start_time': start_time,
                                'end_time': end_time,
                                'room': room,
                                'instructors': instructors,
                                'start_date': start_date,
                                'end_date': end_date
                            })
                
            # Add data to dict
            attrs[class_num] = {
                'index': section_data[0],
                'type': section_data[1],
                'classes' : classes,
            }

        return attrs

    def course_attrs(self):
        """Parses the course attributes out of the page"""

        mapping = {
                "Career": "career",
                "Typically Offered": "typically_offered",
                "Units": "units",
                "Grading Basis": "grading_basis",
                "Add Consent": "add_consent",
                "Drop Consent": "drop_consent",
                "Course Components": "course_components",
                "Enrollment Requirement": "enrollment_requirement",
        }
        
        attrs = {'extra': {}}

        # Get the title and number
        name = self.soup.find("span", {"class": "PALEVEL0SECONDARY"}).string
        m = re.search("^(\S+)\s+(\S+)\s+-\s+(.*)$", name)

        description = ""

        # Blue table with info, enrollment, and description
        info_table = self.soup.find("table", {"class": "SSSGROUPBOXLTBLUEWBO"})

        # Look through inner tables
        inner_tables = self.soup.find_all("table", {"class": "PSGROUPBOXNBO"})
        for table in inner_tables:
            temp = table.find("td", {"class": "SSSGROUPBOXLTBLUE"})
            if not temp or not temp.string:
                continue
            elif temp.string == "Description":
                desc_list = table.find("span", {"class": "PSLONGEDITBOX"}).contents
                if desc_list:
                    # If not x.string, it means it's a <br/> Tag
                    description = "\n".join([x for x in desc_list if x.string])
        
            elif temp.string == "Course Detail":
                # 2 types of labels and datafields

                # Career and grading basis
                labels = table.find_all("label", {"class":"PSDROPDOWNLABEL"})
                data = table.find_all("span", {"class":"PSDROPDOWNLIST_DISPONLY"})
                for x in range(0, len(labels)):
                    if labels[x].string in mapping:
                        attrs['extra'][mapping[labels[x].string]] = data[x].string
                
                # Units and course components
                labels = table.find_all("label", {"class":"PSEDITBOXLABEL"})
                data = table.find_all("span", {"class":"PSEDITBOX_DISPONLY"})
                for x in range(0, len(labels)):
                    if labels[x].string == "Course Components":
                        # Last datafield, has multiple type -> value mappings
                        comp_map = {}
                        for i in range(x, len(data), 2):
                            comp_map[data[i].string] = data[i+1].string

                        attrs['extra'][mapping[labels[x].string]] = comp_map
                        break
                    elif labels[x].string in mapping:
                        attrs['extra'][mapping[labels[x].string]] = data[x].string
                
            elif temp.string == "Enrollment Information":
                # 2 types of labels and datafields
                
                # Add/drop consent
                labels = table.find_all("label", {"class":"PSDROPDOWNLABEL"})
                data = table.find_all("span", {"class":"PSDROPDOWNLIST_DISPONLY"})
                for x in range(0, len(labels)):
                    if labels[x].string in mapping:
                        attrs['extra'][mapping[labels[x].string]] = data[x].string

                # Typically offered, enrollment requirement
                labels = table.find_all("label", {"class":"PSEDITBOXLABEL"})
                data = table.find_all("span", {"class":"PSEDITBOX_DISPONLY"})
                for x in range(0, len(labels)):
                    if labels[x].string in mapping:
                        attrs['extra'][mapping[labels[x].string]] = data[x].string

        attrs['basic'] = {
            'title' : m.group(3),
            'number' : m.group(2),
            'description' : description,
            }
        
        return attrs

    def section_attrs(self):
        """
        Parses the section attributes out of a page.
        Note that information availible on the course page header is not recorded.
        Individual class start/end dates aren't used, just the main one.
        Used for deep scrapes.
        """
        attrs = {
            'details':{
                #'status': open/closed,
                #'session': session,
                #'start_date': datetime object,
                #'end_date': datetime object,
                #'location': course location,
                #'campus': course campus
            },
            'classes':[
                #{
                #    'day_abbr': Mo/Tu/We, etc,
                #    'start_time': datetime object,
                #    'end_time': datetime object
                #    'room': room,
                #    'instructors': [instructor names],
                #}, ...
            ],
            'availability':{
                #'class_max': spaces in class,
                #'class_curr': number enrolled,
                #'wait_max': spaces on wait list,
                #'wait_curr': number waiting
            }
        }

        # Tables for Details, enrollment, availibility, description
        tables = self.soup.find_all("table", {"class": "PSGROUPBOXWBO"})
        for table in tables:
            temp = table.find("td", {"class": "PAGROUPBOXLABELLEVEL1"})
            if not temp or not temp.string:
                continue
            elif temp.string == "Class Details":
                labels = table.find_all("label", {"class": "PSEDITBOXLABEL"})
                data = table.find_all("span", {"class" : "PSEDITBOX_DISPONLY"})
                num_comps = len(data) - len(labels)

                # Store class attributes
                attrs['details']['status'] = data[0].string
                attrs['details']['session'] = data[2].string
                attrs['details']['location'] = data[8 + num_comps].string
                attrs['details']['campus'] = data[9 + num_comps].string

                # Dates
                m = re.search('^([\S]+)\s*-\s*([\S]+)$', data[6 + num_comps].string)
                attrs['details']['start_date'] = datetime.strptime(m.group(1), "%Y/%m/%d") if m else None
                attrs['details']['end_date'] = datetime.strptime(m.group(2), "%Y/%m/%d") if m else None
        
            elif temp.string == "Class Availability":
                data = table.find_all("span", {"class" : "PSEDITBOX_DISPONLY"})
                
                # Store enrollment information
                attrs['availability']['class_max'] = int(data[0].string)
                attrs['availability']['wait_max'] = int(data[1].string)
                attrs['availability']['class_curr'] = int(data[2].string)
                attrs['availability']['wait_curr'] = int(data[3].string)

        # Class time tables
        class_table = self.soup.find("table", id="SSR_CLSRCH_MTG$scroll$0")
        cells = class_table.find_all("span", {"class", "PSLONGEDITBOX"})

        # Iterate over cells in groups of 4 (by line - times, room, instructors, dates)
        for x in range(0, len(cells), 4):
            m = re.search("^(\w\w)\s(\d+:\d+[AP]M)\s*-\s*(\d+:\d+[AP]M)$", cells[x].string)
            attrs['classes'].append({
                'day_abbr': m.group(1) if m else None,
                'start_time': datetime.strptime(m.group(2), "%I:%M%p") if m else None,
                'end_time': datetime.strptime(m.group(3), "%I:%M%p") if m else None,
                'room': cells[x+1].string.strip(),
                # If not i.string, it means it's a Tag, not an instructor
                'instructors': [", ".join(i.strip(", \n").split(",")) for i in cells[x+2].contents if i.string]
            })
        
        return attrs
        

    def enrollment_stats(self):
        """Returns a tuple (capacity, enrolled) containing enrollment stats"""
        capacity_label_holder = self.soup.find("label", { "class": "PSEDITBOXLABEL", "for":"SSR_CLS_DTL_WRK_ENRL_CAP"}, text=re.compile("(Class Capacity)|(Combined Section Capacity)"))

        capacity_index = capacity_label_holder.parent.index(capacity_label_holder)

        capacity = capacity_label_holder.parent.parent.next_sibling.next_sibling.find_all('td')[capacity_index].find('span').text

        enrolled_label_holder = self.soup.find("label", { "class": "PSEDITBOXLABEL", "for":"SSR_CLS_DTL_WRK_ENRL_TOT"}, text=re.compile("Enrollment Total"))
        enrolled_index = enrolled_label_holder.parent.index(enrolled_label_holder)

        enrolled = enrolled_label_holder.parent.parent.next_sibling.next_sibling.find_all('td')[enrolled_index].find('span').text

        return capacity, enrolled

# Testing
"""
with open("tests/course.html") as f:
    data = f.read()
p = SolusParser(data)

print p.course_section_attrs()

#for x in p.all_sections().iteritems():
#    print x
#"""
