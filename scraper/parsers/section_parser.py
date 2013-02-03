import re

import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n

from solus_parser import SolusParser

class SectionParser(SolusParser):

    title_css_class = 'PALEVEL0SECONDARY'

    def sections_are_offered(self):
        """Determines whether there is a 'View class sections' button on the page"""
        return self.soup.find("a", {'id': 'DERIVED_SAA_CRS_SSR_PB_GO'})

    def terms_offered(self, ):
        """Returns the terms during which the current term is offered"""

        terms = []

        term_dropdown = self.soup.find("select", {'id': 'DERIVED_SAA_CRS_TERM_ALT'})

        for option in term_dropdown.find_all("option"):

            m = re.search('^([^\s]+) (.*)$', option.get_text())

            dropdown_value = option['value']
            year = m.group(1)
            season = m.group(2)
            
            # Make a real season
            season = e_or_n(cc.Season, name=season)
            season.save()

            term = e_or_n(cc.Term, year=year, season=season)

            # Store the dropdown value so we can request this term later in scraping
            term.dropdown_value = dropdown_value

            terms.append(term)

        return terms