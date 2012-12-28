import re
from bs4 import BeautifulSoup

class SolusParser(object):
    """Parses Solus's crappy HTML"""

    def __init__(self, text):
        self.soup = BeautifulSoup(text)

    def subject_action(self, subject):
        return self.soup.find("a", title="Show/Hide Courses for Subject", text="%s - %s" % (subject.abbreviation, subject.title))['id']

    def course_action(self, course):
        return self.soup.find("a", { "class": "PSHYPERLINK"}, text=re.compile("%s" % course.number))['id']

    def section_action(self, section):
        return self.soup.find("a", { "class": "PSHYPERLINK"}, title="Class Details", text=re.compile("\(%s\)" % section.solus_id))['id']

    def term_key(self, term):
        return self.soup.find("option", text="%s %s" % (term.year, term.season))['value']

    def enrollment_stats(self):
        capacity_label_holder = self.soup.find("label", { "class": "PSEDITBOXLABEL", "for":"SSR_CLS_DTL_WRK_ENRL_CAP"}, text=re.compile("(Class Capacity)|(Combined Section Capacity)"))

        capacity_index = capacity_label_holder.parent.index(capacity_label_holder)

        capacity = capacity_label_holder.parent.parent.next_sibling.next_sibling.find_all('td')[capacity_index].find('span').text

        enrolled_label_holder = self.soup.find("label", { "class": "PSEDITBOXLABEL", "for":"SSR_CLS_DTL_WRK_ENRL_TOT"}, text=re.compile("Enrollment Total"))
        enrolled_index = enrolled_label_holder.parent.index(enrolled_label_holder)

        enrolled = enrolled_label_holder.parent.parent.next_sibling.next_sibling.find_all('td')[enrolled_index].find('span').text

        return capacity, enrolled



