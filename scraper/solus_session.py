import ssl
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from bs4 import BeautifulSoup

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD

from parsers.alphanum_parser import AlphanumParser
from parsers.subject_parser import SubjectParser
from parsers.course_parser import CourseParser
from parsers.section_parser import SectionParser

class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.
    http://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/
    '''
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version

        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)

class SolusSession(object):
    """Represents a solus browsing session"""

    login_url = "https://my.queensu.ca"
    continue_url = "SAML2/Redirect/SSO" 
    course_catalog_url = "https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_BROWSE_CATLG_P.GBL"

    #State of recovery ( < 0 is not recovering, otherwise the current recovery level)
    recovery_state = -1
    #letter, subj subject, course, term, section
    recovery_stack = [None, None, None, None, None]

    def __init__(self, user=None, password=None):
        self.session = requests.session()
        # Use SSL version 1
        self.session.mount('https://', SSLAdapter(ssl_version=ssl.PROTOCOL_TLSv1))

        self.latest_response = None
        self.latest_text = None
        self._soup = None

        print"Logging in...") 
        self.login(user, password)

        print("Navigating to course catalog...")
        self.go_to_course_catalog()

        # Should now be on the course catalog page. If not, something went wrong
        if self.latest_response.url != self.course_catalog_url:
            raise Exception("Authenticated, but couldn't access the SOLUS course catalog.")

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

        # Load the access page to set all the cookies and get redirected
        self._get(self.login_url)

        # Login procedure is differnt when JS is disabled
        payload = {
           'j_username': user,
           'j_password': password,
           'IDButton': '%C2%A0Log+In%C2%A0',
        }
        self._post(self.latest_response.url, data=payload)
       
        # Check for the continue page
        if self.continue_url in self.latest_response.url:
            self.do_continue_page()
        
        # Should now be authenticated and on the my.queensu.ca page, submit a request for the URL in the 'SOLUS' button
        link = self.soup.find("a", text="SOLUS")
        if not link:
            # Not on the right page
            raise Exception("Could not authenticate with the Queen's SSO system. The login credentials provided in private_config.py may have been incorrect.")

        print ("Sucessfully authenticated.")
        # Have to actually use this link to access SOLUS initially otherwise it asks for login again
        self._get(link.get("href"))

        # The request could (seems 50/50 from browser tests) bring up another continue page
        if self.continue_url in self.latest_response.url:
            self.do_continue_page()

        # Should now be logged in and on the student center page


    def do_continue_page(self):
        """
        The SSO system returns a specific page only if JS is disabled
        It has you click a Continue button which submits a form with some hidden values
        """
        
        #Grab the RelayState, SAMLResponse, and POST url
        form = self.soup.find("form")
        if not form:
            # No form, nothing to be done
            return
        url = form.get("action")

        payload = {}
        for x in form.find_all("input", type="hidden"):
            payload[x.get("name")] = x.get("value")

        self._post(url, data=payload)


    def go_to_course_catalog(self):
        self._catalog_post("")
        self.select_alphanum("A")

    # ----------------------------- Alphanums ------------------------------------ #

    def select_alphanum(self, alphanum):
        """Navigates to a letter/number"""
        if self.recovery_state < 0:
            self.recovery_stack[0] = alphanum

        self._catalog_post('DERIVED_SSS_BCC_SSR_ALPHANUM_' + alphanum.upper())

    # ----------------------------- Subjects ------------------------------------- #

    def subject_from_dropdown(self, subject_index):
        """Returns the subject with the specified index on the current alphanum's page, or none if the dropdown index does not exist"""
        return AlphanumParser(self.soup).subject_from_dropdown(subject_index)
       
    def dropdown_subject(self, subject):
        """Opens the dropdown menu for a subject"""
        if self.recovery_state < 0:
            self.recovery_stack[1] = subject

        self._catalog_post(subject.click_action)

    def rollup_subject(self, subject):
        """Closes the dropdown menu for a subject"""
        if self.recovery_state < 0:
            self.recovery_stack[1] = None

        self._catalog_post(subject.click_action)

    # ----------------------------- Courses ------------------------------------- #

    def course_link_exists(self, course_index):
        """Returns whether or not a course link with the specified index exists"""
        return SubjectParser(self.soup).course_link_exists(course_index)
       
    def open_course(self, course_index):
        """Opens a course page by following the course link with the supplied index"""
        if self.recovery_state < 0:
            self.recovery_stack[2] = course_index
        
	action = SubjectParser(self.soup).course_link_id(course_index)
        self._catalog_post(action)

    def current_course(self, subject):
        """Returns the course built from the current course page"""
        return CourseParser(self.soup).current_course(subject)

    def return_from_course(self):
        """Navigates back from course to subject"""
        self.recovery_stack[3] = None
        self.recovery_stack[2] = None
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
        if self.recovery_state < 0:
            self.recovery_stack[3] = term
        
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
        if self.recovery_state < 0:
            self.recovery_stack[4] = section

        self._catalog_post(section.click_action)
    
    def scrape_section_page(self, section):
        """Adds the information available on the dedicated section page to the provided section"""
        return SectionParser(self.soup).add_section_page_attributes(section)

    def return_from_section(self):
        """Navigates back from section to course"""
        self.recovery_stack[4] = None
        self._catalog_post('CLASS_SRCH_WRK2_SSR_PB_CLOSE')


    # -----------------------------General Purpose------------------------------------- #

    def _get(self, url, **kwargs):
        self.latest_response = self.session.get(url, **kwargs)
        self._update_attrs()
    
    def _post(self, url, **kwargs):
        self.latest_response = self.session.post(url, **kwargs)
        self._update_attrs()

    def _update_attrs(self):
        self.latest_text = self.latest_response.text
        
        # The old soup no longer represents the current page's content
        self._soup = None

    def _catalog_post(self, action, extras={}):
        """Submits a post request to the site"""
        extras['ICAction'] = action
        self._post(self.course_catalog_url, data=extras)

        #import random
        # TODO: Improve this, could easily give false positives
        if "Data Integrity Error" in self.latest_text:
            self._recover(action, extras)
            #raise Exception("SOLUS reported a Data Integrity Error")

        # TESTING - Fake a DIE using random number generator
        #elif action != "" and random.random() < 0.1:
        #    self._catalog_post("")
        #    self._recover(action, extras)

    def _recover(self, action, extras={}):
        """Attempts to recover the scraper state after encountering an error"""

        # Don't recurse, retry
        if self.recovery_state >= 0:
            print ("Error while recovering, retrying")
            self.recovery_state = 0
            return

        # Number of non-null elements in the recovery stack
        num_states = len(filter(None, self.recovery_stack))

        # Start recovery process
        print ("-----------------------------------")
        print ("Encounted SOLUS Data Integrety Error, attempting to recover")
        self.recovery_state = 0

        while self.recovery_state < num_states:

            # Has to be done before the recovery operations
            self.recovery_state += 1

            # State numbers are OBO due to previous increment
            if self.recovery_state == 1:
                print ("--Selecting letter {0}".format(self.recovery_stack[0]))
                self.select_alphanum(self.recovery_stack[0])
            elif self.recovery_state == 2:
                print ("----Selecting subject {0}".format(self.recovery_stack[1]))
                self.dropdown_subject(self.recovery_stack[1])
            elif self.recovery_state == 3:
                print ("------Selecting course number {0}".format(self.recovery_stack[2]))
                self.open_course(self.recovery_stack[2])
                self.show_sections()
            elif self.recovery_state == 4:
                print ("--------Selecting term {0}".format(self.recovery_stack[3]))
                self.switch_to_term(self.recovery_stack[3])
            elif self.recovery_state == 5:
                print ("----------Selecting section {0}".format(self.recovery_stack[4]))
                self.visit_section_page(self.recovery_stack[4])

        # Finished recovering
        self.recovery_state = -1
        print ("Recovered, retrying original request")
        print ("-----------------------------------")

        self._catalog_post(action, extras)
