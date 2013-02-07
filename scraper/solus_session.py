import requests
from bs4 import BeautifulSoup

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD

from parsers.alphanum_parser import AlphanumParser
from parsers.subject_parser import SubjectParser
from parsers.course_parser import CourseParser
from parsers.section_parser import SectionParser

class SolusSession(object):
    """Represents a solus browsing session"""

    login_url = "https://sso.queensu.ca/amserver/UI/Login"
    course_catalog_url = "https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_BROWSE_CATLG_P.GBL"

    def __init__(self, user=None, password=None):
        self.session = requests.session()

        self.latest_response = None
        self.latest_text = None
        self._soup = None

        print "Logging in..."    
        self.login(user, password)

        print "Navigating to course catalog..."
        self.go_to_course_catalog()

    @property
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self.latest_text, 'lxml')
        return self._soup

    def login(self, user=None, password=None):
        """Logs into the site"""

        # Check for supplied credentials
        if not user:
            user = SCRAPER_USERNAME
        if not password:
            password = SCRAPER_PASSWORD

        payload = {
           'IDToken1': user,
           'IDToken2': password,
           'IDButton': 'Submit',
           }

        response = self.session.post(self.login_url, data=payload)

        if len(response.text) < 200 or "Invalid Password!" in response.text:
            raise Exception("Could not log in to SOLUS. The login credentials provided in private_config.py may have been incorrect.")

    def go_to_course_catalog(self):
        self._catalog_post("")
        self.select_alphanum("A")

    def _catalog_post(self, action, extras={}):
        """Submits a post request to the site"""

        extras['ICAction'] = action
        self.latest_response = self.session.post(self.course_catalog_url, data=extras)
        self.latest_text = self.latest_response.text

        # The old soup no longer represents the current page's content
        self._soup = None

        if "Data Integrity Error" in self.latest_text:
            raise Exception("SOLUS reported a Data Integrity Error")

    # ----------------------------- Alphanums ------------------------------------ #

    def select_alphanum(self, alphanum):
        """Navigates to a letter/number"""
        self._catalog_post('DERIVED_SSS_BCC_SSR_ALPHANUM_' + alphanum.upper())

    # ----------------------------- Subjects ------------------------------------- #

    def subject_from_dropdown(self, subject_index):
        """Returns the subject with the specified index on the current alphanum's page, or none if the dropdown index does not exist"""
        return AlphanumParser(self.soup).subject_from_dropdown(subject_index)
       
    def toggle_subject_dropdown(self, subject):
        """Opens or closes the dropdown menu for a subject"""
        self._catalog_post(subject.click_action)


    # ----------------------------- Courses ------------------------------------- #

    def course_link_exists(self, course_index):
        """Returns whether or not a course link with the specified index exists"""
        return SubjectParser(self.soup).course_link_exists(course_index)
       
    def open_course(self, course_index):
        """Opens a course page by following the course link with the supplied index"""
        action = SubjectParser(self.soup).course_link_id(course_index)
        self._catalog_post(action)

    def current_course(self, subject):
        """Returns the course built from the current course page"""
        return CourseParser(self.soup).current_course(subject)

    def return_from_course(self):
        """Navigates back from course to subject"""
        self._catalog_post('DERIVED_SAA_CRS_RETURN_PB')

    # -----------------------------Sections ------------------------------------- #

    def sections_are_offered(self):
        """Determines whether there is a 'View class sections' button on the page"""
        return SectionParser(self.soup).sections_are_offered()

    def show_sections(self):
        """Clicks on the 'View class sections' button on the course page"""
        self._catalog_post('DERIVED_SAA_CRS_SSR_PB_GO')

    def terms_offered(self):
        """Returns the terms during which the current course is offered"""
        return SectionParser(self.soup).terms_offered()

    def switch_to_term(self, term):
        """Shows the sections for a given term"""
        self._catalog_post(action='DERIVED_SAA_CRS_SSR_PB_GO$92$', extras={'DERIVED_SAA_CRS_TERM_ALT': term.dropdown_value})

    def multiple_section_pages_available(self):
        """Returns whether or not there is a "view all sections" button on the page"""
        return SectionParser(self.soup).view_all_section_button_exists()

    def view_all_sections(self):
        """Presses the "view all sections" link on the course page"""
        self._catalog_post('CLASS_TBL_VW5$fviewall$0')

    def current_sections(self, course, term):
        """Returns all sections visible on the current course page"""
        return SectionParser(self.soup).current_sections(course, term)

    def visit_section_page(self, section):
        """Opens the dedicated page for the provided section"""
        self._catalog_post(section.click_action)

    def scrape_section_page(self, section):
        """Adds the information available on the dedicated section page to the provided section"""
        return SectionParser(self.soup).add_section_page_attributes(section)

    def return_from_section(self):
        """Navigates back from section to course"""
        self._catalog_post('CLASS_SRCH_WRK2_SSR_PB_CLOSE')
