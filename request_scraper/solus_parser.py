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

    def section_link(self, solus_id):
        """Returns the id of the link to the section on the course page"""
        return self.soup.find("a", { "class": "PSHYPERLINK"}, title="Class Details", text=re.compile("\(%s\)" % solus_id))['id']

    def term_key(self, year, season):
        #TODO: deprectate for all_terms
        """Returns the key of the term from the term select combobox"""
        return self.soup.find("option", text="%s %s" % (year, season))['value']

    #######
    # Get data for all object POSTs (subject, course, etc)
    #######

    def all_subjects(self):
        """
        Returns a dict of subject data in the current letter
        Format = {abbreviation: (title, dropdown id)}
        """
        ret = {}
        for tags in self.soup.find_all("a", title="Show/Hide Courses for Subject"):
            abbr, sbj = tags.string.split(" - ")
            ret[abbr] = (sbj, tags['id'])
        return ret

    def all_courses(self):
        """
        Returns a dict of course data in the expanded subject(s)
        Format = {number: (name, link id)}
        """
        ret = {}
        for x in self.soup.find_all("a", { "class": "PSHYPERLINK"}):
            # Get a number, then the title
            if "CRSE_TITLE" in x['id']:
                # There are somtimes tags inside the titles
                ret[temp] = ("".join([i for i in x.stripped_strings]).strip(), x['id'])
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
        Format = {class number: (index, type, id)}
        """
        ret = {}
        for x in self.soup.find_all("a", {"class": "PSHYPERLINK", "title": "Class Details"}):
            m = re.search('(\S+)-(\S+)\s+\((\S+)\)', x.string)
            ret[m.group(3)] = (m.group(1), m.group(2), x['id'])
        return ret

    #######
    # Get information
    #######

    def course_attrs(self):
        """Parses the course attributes out of the page"""

        attrs = {}

        # Get the title and number
        name = self.soup.find("span", {"class": "PALEVEL0SECONDARY"}).string
        m = re.search("^(\S+)\s+(\S+)\s+-\s+(.*)$", name)

        #Get the description
        description = ""

        # Blue table with info, enrollment, and description (maybe)
        info_table = self.soup.find("table", {"class": "SSSGROUPBOXLTBLUEWBO"})

        # Look through inner tables
        inner_tables = self.soup.find_all("table", {"class": "PSGROUPBOXNBO"})
        for table in inner_tables:
            temp = table.find("td", {"class": "SSSGROUPBOXLTBLUE"})
            if not temp:
                continue
            elif temp.string == "Description":
                desc_list = self.soup.find("span", {"class": "PSLONGEDITBOX"}).contents
                if desc_list:
                    # If not x.string, it means it's a <br/> Tag
                    description = "\n".join([x for x in desc_list if x.string])
        
            # TODO: Implement extra info:
            elif temp.string == "Course Detail":
                pass
                # PSDROPDOWNLABEL (career, grading basis)
                # PSDROPDOWNLIST_DISPONLY (career, grading basis)
                
                # PSEDITBOXLABEL (units, course components)
                # PSEDITBOX_DISPONLY (units, course_reqs(type, required/not))
            elif temp.string == "Enrollment Information":
                pass
                # PSDROPDOWNLABEL (add/drop consent)
                # PSDROPDOWNLIST_DISPONLY (add/drop consent)

                # PSEDITBOXLABEL (typically offered, enrollment requirement)
                # PSEDITBOX_DISPONLY (typically offered, enrollment requirement)

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
        # PSEDITBOX_DISPONLY = class detail fields and class availiblity fields
        # PSEDITBOX_LABEL = labels for PSEDITBOX_DISPONLY fields + 1 for enrollment (if it exists)
        # Class component has 1 label, but multiple (n*2) fields - (type + required) * n
        data = self.soup.find_all("span", {"class" : "PSEDITBOX_DISPONLY"})
        labels = self.soup.find_all("label", {"class": "PSEDITBOXLABEL"})
        num_comps = len(data) - len(labels)

        # If enrollment label exists, alter the offset
        for x in labels:
            if x.string == "Enrollment Requirements":
                num_comps += 1
        
        # Store class attributes
        attrs['details']['status'] = data[0].string
        attrs['details']['session'] = data[2].string
        attrs['details']['location'] = data[8 + num_comps].string
        attrs['details']['campus'] = data[9 + num_comps].string

        # Dates
        m = re.search('^([\S]+)\s*-\s*([\S]+)$', data[6 + num_comps].string)
        attrs['details']['start_date'] = datetime.strptime(m.group(1), "%Y/%m/%d")
        attrs['details']['end_date'] = datetime.strptime(m.group(2), "%Y/%m/%d")

        # Store enrollment information
        attrs['availability']['class_max'] = int(data[10 + num_comps].string)
        attrs['availability']['wait_max'] = int(data[11 + num_comps].string)
        attrs['availability']['class_curr'] = int(data[12 + num_comps].string)
        attrs['availability']['wait_curr'] = int(data[13 + num_comps].string)

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
                'instructors': [i.strip(", \n") for i in cells[x+2].contents if i.string]
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

print p.course_attrs()

#for x in p.all_sections().iteritems():
#    print x
#"""
