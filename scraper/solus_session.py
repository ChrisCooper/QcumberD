import requests

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD


class SolusSession(object):
    """Represents a solus browsing session"""

    login_url = "https://sso.queensu.ca/amserver/UI/Login"
    course_catalog_url = "https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_BROWSE_CATLG_P.GBL"

    def __init__(self, user=None, password=None):
        self.session = requests.session()

        self.latest_response = None
        self.latest_text = ''

        print "Logging in..."    
        self.login(user, password)

        print "Navigating to course catalog..."
        self.go_to_course_catalog()

    def close_session(self):
        self.session.close()

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

    def _catalog_post(self, action, extras={}):
        """Submits a post request to the site"""
        if not action:
            return

        extras['ICAction'] = action
        self.latest_response = self.session.post(self.course_catalog_url, data=extras)
        self.latest_text = self.latest_response.text

        if "Data Integrity Error" in self.latest_text:
            raise Exception("SOLUS reported a Data Integrity Error")