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

        # Scrape the sections in each term
        for term in terms:

            term.save(was_scraped=True)

            # View the sections for this term
            self.solus.switch_to_term(term)

            self.scrape_sections_in_term(term, course)

    def scrape_sections_in_term(self, term, course):

        if self.solus.multiple_section_pages_available():
            self.solus.view_all_sections()

        sections = self.solus.current_sections(course, term)

        for section in sections:

            #Check if we should visit the section page
            if self.config.deep:
                self.solus.visit_section_page(section)
                self.solus.scrape_section_page(section)
                self.solus.return_from_section()

            section.save(was_scraped=True)
