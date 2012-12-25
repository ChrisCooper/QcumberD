import requests, re
from bs4 import BeautifulSoup

from qcumber.config import MISSING_MODULE_MESSAGE

try:
    import untracked
except ImportError as e:
    raise ImportError(MISSING_MODULE_MESSAGE)

class SolusSession(object):

    login_url = "https://sso.queensu.ca/amserver/UI/Login"
    course_catalog_url = "https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_BROWSE_CATLG_P.GBL"

    def __init__(self):
        self.session = requests.session()
        self.latest_response = None
        self.latest_text = ''

    def scrape_enrollment(self, section):
        course = section.course

        self.navigate_to_course(course)

        self.show_sections()

        self.switch_terms(section.term)

        self.show_all_sections()

        self.view_section(section)

        capacity, enrolled = SolusParser(self.latest_text).enrollment_stats()

        self.return_from_section()

        self.return_from_course()

        return capacity, enrolled 


    def navigate_to_course(self, course):
        subject = course.subject

        self.login()

        self.select_alphanum(subject.abbreviation[:1])
        self.select_alphanum(subject.abbreviation[:1])

        self.dropdown_subject(subject)

        self.select_course(course)

    def login(self):

        payload = {
           'IDToken1': untracked.username,
           'IDToken2': untracked.password,
           'IDButton': 'Submit',
           }

        response = self.session.post(SolusSession.login_url, data=payload)

        if len(response.text) < 200:
            raise Exception("Could not log in to SOLUS. The login credentials provided in untracked.py may have been incorrect.")

        return response

    def select_alphanum(self, alphanum):
        return self._catalog_post('DERIVED_SSS_BCC_SSR_ALPHANUM_' + alphanum.upper())

    def dropdown_subject(self, subject):
        action = SolusParser(self.latest_text).subject_action(subject)

        return self._catalog_post(action)

    def select_course(self, course):
        action = SolusParser(self.latest_text).course_action(course)
        return self._catalog_post(action)

    def view_section(self, section):
        action = SolusParser(self.latest_text).section_action(section)
        return self._catalog_post(action)

    def show_sections(self):
        return self._catalog_post('DERIVED_SAA_CRS_SSR_PB_GO')

    def switch_terms(self, term):
        term_key = SolusParser(self.latest_text).term_key(term)
        return self._catalog_post('DERIVED_SAA_CRS_SSR_PB_GO$92$', extras={'DERIVED_SAA_CRS_TERM_ALT': term_key})

    def show_all_sections(self):
        return self._catalog_post('CLASS_TBL_VW5$fviewall$0')

    def return_from_section(self):
        return self._catalog_post('CLASS_SRCH_WRK2_SSR_PB_CLOSE')

    def return_from_course(self):
        return self._catalog_post('DERIVED_SAA_CRS_RETURN_PB')

    def _catalog_post(self, action, extras={}):
        extras['ICAction'] = action
        self.latest_response = self.session.post(SolusSession.course_catalog_url, data=extras)
        self.latest_text = self.latest_response.text


class SolusParser(object):

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




