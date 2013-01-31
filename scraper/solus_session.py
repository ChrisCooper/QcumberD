# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests

from solus_parser import SolusParser

class SolusSession(object):
    """Represents a solus browsing session"""

    login_url = "https://sso.queensu.ca/amserver/UI/Login"
    course_catalog_url = "https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_BROWSE_CATLG_P.GBL"

    #State of recovery ( < 0 is not recovering, otherwise the current recovery level)
    recovery_state = -1
    #letter, subj (abbr, title), course, term (year, season), section
    recovery_stack = [None, None, None, None, None]

    def __init__(self, user, password):
        self.session = requests.session()

        self.latest_response = None
        self.latest_text = ''

        print "Logging in..."
        self.login(user, password)
        print "Logged in"

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

        if len(response.text) < 200 or "Invalid Password!" in response.text:
            raise Exception("Could not log in to SOLUS. The login credentials provided in private_config.py may have been incorrect.")

        # Go to the course catalog after logging in
        self._catalog_post("")

    def select_alphanum(self, alphanum):
        """Navigates to a letter/number"""
        if self.recovery_state < 0:
            self.recovery_stack[0] = alphanum

        self._catalog_post('DERIVED_SSS_BCC_SSR_ALPHANUM_' + alphanum.upper())

    def dropdown_subject(self, abbr, title):
        """Opens the dropdown menu for a subject"""
        if self.recovery_state < 0:
            self.recovery_stack[1] = (abbr, title)

        action = self.parser().subject_dropdown(abbr, title)
        self._catalog_post(action)

    def rollup_subject(self, abbr, title):
        """Closes the dropdown menu for a subject"""
        if self.recovery_state < 0:
            self.recovery_stack[1] = None

        action = self.parser().subject_dropdown(abbr, title)
        self._catalog_post(action)

    def select_course(self, number):
        """Clicks on a course"""
        if self.recovery_state < 0:
            self.recovery_stack[2] = number

        action = self.parser().course_link(number)
        self._catalog_post(action)

    def view_section(self, class_num):
        """Clicks on a course section"""
        if self.recovery_state < 0:
            self.recovery_stack[4] = class_num

        action = self.parser().section_link(class_num)
        self._catalog_post(action)

    def show_sections(self):
        """Clicks on the 'View class sections' button on the course page"""
        self._catalog_post('DERIVED_SAA_CRS_SSR_PB_GO')

    def switch_terms(self, year, season):
        """Shows the sections for a term of the class"""
        if self.recovery_state < 0:
            self.recovery_stack[3] = (year, season)

        term_key = self.parser().term_key(year, season)
        self._catalog_post(action='DERIVED_SAA_CRS_SSR_PB_GO$92$', extras={'DERIVED_SAA_CRS_TERM_ALT': term_key})

    def show_all_sections(self):
        """Clicks the 'view all' button"""
        self._catalog_post('CLASS_TBL_VW5$fviewall$0')

    def return_from_section(self):
        """Navigates back from section to course"""
        self.recovery_stack[4] = None

        self._catalog_post('CLASS_SRCH_WRK2_SSR_PB_CLOSE')

    def return_from_course(self):
        """Navigates back from course to subject"""
        self.recovery_stack[3] = None
        self.recovery_stack[2] = None

        self._catalog_post('DERIVED_SAA_CRS_RETURN_PB')

    def parser(self):
        """Returns a SolusParser instance for the current page"""
        return SolusParser(self.latest_text)

    def _catalog_post(self, action, extras={}):
        """Submits a post request to the site"""
        extras['ICAction'] = action
        self.latest_response = self.session.post(self.course_catalog_url, data=extras)
        self.latest_text = self.latest_response.text

        # Improve this, could easily give false positives
        if "Data Integrity Error" in self.latest_text:
            self._recover(action, extras)
            #raise Exception("SOLUS reported a Data Integrity Error")

        # TESTING - Fake a DIE using random number generator
        #import random
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
                print ("----Selecting subject {0} - {1}".format(*self.recovery_stack[1]))
                self.dropdown_subject(*self.recovery_stack[1])
            elif self.recovery_state == 3:
                print ("------Selecting course number {0}".format(self.recovery_stack[2]))
                self.select_course(self.recovery_stack[2])
                self.show_sections()
            elif self.recovery_state == 4:
                print ("--------Selecting term {0} {1}".format(*self.recovery_stack[3]))
                self.switch_terms(*self.recovery_stack[3])
            elif self.recovery_state == 5:
                print ("----------Selecting section {0}".format(self.recovery_stack[4]))
                self.view_section(self.recovery_stack[4])

        # Finished recovering
        self.recovery_state = -1
        print ("Recovered, retrying original request")
        print ("-----------------------------------")

        self._catalog_post(action, extras)