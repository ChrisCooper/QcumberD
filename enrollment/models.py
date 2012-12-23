import requests
from BeautifulSoup import BeautifulSoup

import untracked

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
        self.show_all_sections()
        self.view_section(section)
        capacity, enrolled = SolusParser(self.latest_text).enrollment_stats()


    def navigate_to_course(self, course):
        subject = course.subject

        self.login()
        self.select_alphanum(subject.abbreviation[:1])
        self.dropdown_subject(subject)
        self.select_course(course)

    def login(self):

        payload = {
           'IDToken1': untracked.username,
           'IDToken2': untracked.password,
           'IDButton': 'Submit',
           }

        return self.session.post(Solus.login_url, data=payload)

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

    def show_sections(self, index):
        return self._catalog_post('DERIVED_SAA_CRS_SSR_PB_GO')

    def show_all_sections(self, index):
        return self._catalog_post('CLASS_TBL_VW5$fviewall$0')

    def return_from_course(self, index):
        return self._catalog_post('DERIVED_SAA_CRS_RETURN_PB')

    def _catalog_post(self, action):
        self.latest_response = self.session.post(Solus.course_catalog_url, data={'ICAction': action})
        self.latest_text = self.latest_response.text


class SolusParser(object):

    def __init__(self, text):
        self.soup = BeautifulSoup(text)

    def subject_action(self, subject):
        return 'DERIVED_SSS_BCC_GROUP_BOX_1$84$$4'

    def course_action(self, course):
        return 'CRSE_TITLE$5'

    def section_action(self, section):
        'CLASS_SECTION$0'

    def enrollment_stats(self):
        print self.soup.prettify()
        return 0,0
        

