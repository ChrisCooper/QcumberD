from solus_scraper import SolusScraper
#from section_component_scraper import SectionComponentScraper

class SectionScraper(SolusScraper):

    def scrape_all_sections(self, course):
        """Scrapes all sections for the current course"""

        if not self.solus.sections_are_offered():
            # There are no sections to scrape
            return

        self.solus.show_sections()

        terms = self.solus.terms_offered()

        for term in terms:
             term.save()
             self.solus.switch_to_term(term)
        
        #     view all sections
        #     scrape sections
        #         if deepscrape:
        #             visit section page


        return