import requests

from solus_parser import SolusParser

class SolusSession(object):
    """Represents a solus browsing session"""

    login_url = "https://sso.queensu.ca/amserver/UI/Login"
    course_catalog_url = "https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_BROWSE_CATLG_P.GBL"

    def __init__(self, user, password):
        self.session = requests.session()

        self.latest_response = None
        self.latest_text = ''
        self.login(user, password)

    def close_session(self):
        self.session.close()

    def login(self, user, password):
        """Logs into the site"""

        payload = {
           'IDToken1': user,
           'IDToken2': password,
           'IDButton': 'Submit',
           }

        response = self.session.post(self.login_url, data=payload)

        if len(response.text) < 200:
            raise Exception("Could not log in to SOLUS. The login credentials provided in private_config.py may have been incorrect.")

        return response

    def navigate_to_course(self, course):
        """Navigates to a course"""

        subject = course.subject

        self.select_alphanum(subject.abbreviation[:1])
        self.select_alphanum(subject.abbreviation[:1])

        self.dropdown_subject(subject)

        self.select_course(course)

    def select_alphanum(self, alphanum):
        """Navigates to a letter/number"""
        return self._catalog_post('DERIVED_SSS_BCC_SSR_ALPHANUM_' + alphanum.upper())

    def dropdown_subject(self, subject):
        """Opens the dropdown menu for a subject"""
        action = self.parser().subject_dropdown(subject)

        return self._catalog_post(action)

    def select_course(self, course):
        """Clicks on a course"""
        action = self.parser().course_link(course)
        return self._catalog_post(action)

    def view_section(self, section):
        """Clicks on a course section"""
        action = self.parser().section_link(section)
        return self._catalog_post(action)

    def show_sections(self):
        """Clicks on the 'View class sections' button on the course page"""
        return self._catalog_post('DERIVED_SAA_CRS_SSR_PB_GO')

    def switch_terms(self, term):
        """Shows the sections for a term of the class"""
        term_key = self.parser().term_key(term)
        return self._catalog_post('DERIVED_SAA_CRS_SSR_PB_GO$92$', extras={'DERIVED_SAA_CRS_TERM_ALT': term_key})

    def show_all_sections(self):
        """Clicks the 'view all' button"""
        return self._catalog_post('CLASS_TBL_VW5$fviewall$0')

    def return_from_section(self):
        """Navigates back from section to course"""
        return self._catalog_post('CLASS_SRCH_WRK2_SSR_PB_CLOSE')

    def return_from_course(self):
        """Navigates back from course to subject"""
        return self._catalog_post('DERIVED_SAA_CRS_RETURN_PB')

    def parser(self):
        """Returns a SolusParser instance for the current page"""
        return SolusParser(self.latest_text)

    def _catalog_post(self, action, extras={}):
        """Submits a post request to the site"""
        extras['ICAction'] = action
        self.latest_response = self.session.post(self.course_catalog_url, data=extras)
        self.latest_text = self.latest_response.text
