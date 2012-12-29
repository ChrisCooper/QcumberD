import re
from bs4 import BeautifulSoup

class SolusParser(object):
    """Parses Solus's crappy HTML"""

    def __init__(self, text):
        """Initilizes an instance of BeautifulSoup"""
        self.soup = BeautifulSoup(text)

    #######
    # Get data for POST requests (for a known object)
    #######

    def subject_dropdown(self, subject):
        """Returns the id of the subject dropdown link"""
        return self.soup.find("a", title="Show/Hide Courses for Subject", text="%s - %s" % (subject.abbreviation, subject.title))['id']

    def course_link(self, course):
        """Returns the id of the course link in the subject dropdown"""
        return self.soup.find("a", { "class": "PSHYPERLINK"}, text=re.compile("%s" % course.number))['id']

    def section_link(self, section):
        """Returns the id of the link to the section on the course page"""
        return self.soup.find("a", { "class": "PSHYPERLINK"}, title="Class Details", text=re.compile("\(%s\)" % section.solus_id))['id']

    def term_key(self, term):
        """Returns the key of the term from the term select combobox"""
        return self.soup.find("option", text="%s %s" % (term.year, term.season))['value']

    #######
    # Get data for all object POSTs (subject, course, etc)
    #######

    def all_subjects(self):
        """
        Returns a dict of subject data in the current letter
        Format = {abbreviation: (name, dropdown id)}
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
                ret[temp] = (x.string.strip(), x['id'])
            elif "CRSE_NBR" in x['id']:
                temp = x.string.strip()
        return ret

    def all_terms(self):
        """
        Returns a dict containing term data in the current course
        Format = {name: value}
        """
        ret = {}
        term_sel = self.soup.find("select", id="DERIVED_SAA_CRS_TERM_ALT")
        for x in term_sel.find_all("option"):
            ret[x.string] = x['id']
        return ret
        
    def all_sections(self):
        """
        Returns a dict containing data for sections in the current term
        Format = {name: id}
        """
        ret = {}
        for x in self.soup.find_all("a", {"class": "PSHYPERLINK", "title": "Class Details"}):
            ret[x.string] = x['id']
        return ret

    #######
    # Get information
    #######

    def enrollment_stats(self):
        """Returns a tuple (capacity, enrolled) containing enrollment stats"""
        capacity_label_holder = self.soup.find("label", { "class": "PSEDITBOXLABEL", "for":"SSR_CLS_DTL_WRK_ENRL_CAP"}, text=re.compile("(Class Capacity)|(Combined Section Capacity)"))

        capacity_index = capacity_label_holder.parent.index(capacity_label_holder)

        capacity = capacity_label_holder.parent.parent.next_sibling.next_sibling.find_all('td')[capacity_index].find('span').text

        enrolled_label_holder = self.soup.find("label", { "class": "PSEDITBOXLABEL", "for":"SSR_CLS_DTL_WRK_ENRL_TOT"}, text=re.compile("Enrollment Total"))
        enrolled_index = enrolled_label_holder.parent.index(enrolled_label_holder)

        enrolled = enrolled_label_holder.parent.parent.next_sibling.next_sibling.find_all('td')[enrolled_index].find('span').text

        return capacity, enrolled
