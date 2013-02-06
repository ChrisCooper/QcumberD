import requests
from bs4 import BeautifulSoup

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD

class ExamScraper(object):
    """Superclass for scraping exam data"""

    login_url = "http://proxy.queensu.ca/login"
    scrape_url = "http://library.queensu.ca/examsearch"
    
    def __init__(self, config, user=None, password=None):
        self.session = requests.session()

        print "Logging in..."    
        self.login(user, password)
        print "Logged in"

    def login(self, user=None, password=None):
        """Logs into the proxy"""

        # Check for supplied credentials
        if not user:
            user = SCRAPER_USERNAME
        if not password:
            password = SCRAPER_PASSWORD

        payload = {
           'user': user,
           'pass': password,
           'url': self.scrape_url,
           'cmd': "authenticate",
           'Login': "Connect+from+Off-Campus"
           }

        response = self.session.post(self.login_url, data=payload)

        if len(response.text) < 200 or "Login failed" in response.text:
            raise Exception("Could not log in to Exambank. The login credentials provided in private_config.py may have been incorrect.")

        self.soup = BeautifulSoup(response.text)    

    def scrape(self):
        years = self.soup.find("select", {"name": "year"}).find_all("option", value=True)
        for x in years:
            if "value" in x:
                year = x["value"]
                print ("Scraping year: " + year)