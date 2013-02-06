# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import requests
from bs4 import BeautifulSoup

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD

from course_catalog.models import existing_or_new, Subject, Course, CourseRelation
from models import Exam
from django.core.exceptions import ObjectDoesNotExist

class ExamScraper(object):
    """Superclass for scraping exam data"""

    login_url = "http://proxy.queensu.ca/login"
    scrape_url = "http://library.queensu.ca/examsearch/index.php"
    
    def __init__(self, config, user=None, password=None):
        self.session = requests.session()
        self.config = config

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

    def _store_data(self, year, match):
        if not match:
            return

        # Check if there are any courses to attach the exam to
        try:
            subject = Subject.objects.get(abbreviation=match.groups()[0].upper())
            courses = Course.objects.filter(subject=subject, number__istartswith=match.groups()[1])
            num_courses = courses.count()
        except ObjectDoesNotExist:
            num_courses = 0

        if num_courses < 1:
            print ("--No course '{0} {1}' in database".format(match.groups()[0], match.groups()[1]))
            return

        # Find/Create the course <-> data relation(s)
        course_relations = []
        for course in courses:
            temp = existing_or_new(CourseRelation, course=course)
            temp.save()
            course_relations.append(temp)

        exam_attrs = {
                    "year": year,
                    "pdf_url": "http://library.queensu.ca" + match.string}

        exam = existing_or_new(Exam, **exam_attrs)
        for course_relation in course_relations:
            exam.course_rels.add(course_relation)
        exam.save()
        print ("--Added exam pdf for {0} course(s): {1}".format(num_courses, ", ".join([str(course) for course in courses])))

    def _parse_url(self, year, url):

        m = re.match("/exambank/\d+/(\D+)(\d+).*\.pdf", url)
        if m:
            self._store_data(year, m)

    def scrape(self):

        print ("Starting scrape")

        years = self.soup.find("select", {"name": "year"}).find_all("option", value=True)
        for x in years[self.config.year_start_idx:self.config.year_end_idx]:

            year = x.get("value", None)
            if not year:
                continue

            print ("Scraping year: " + year)

            r = self.session.post(self.scrape_url, data={"year": year, "submit": "Search Exambank"})

            self.soup = BeautifulSoup(r.text)

            table = self.soup.find("table", {"class": "tablesort"})
            links = table.find_all("a", href=True, text="Download")

            for link in links:
                url = link.get("href", None)
                if not url:
                    continue

                self._parse_url(year, url)