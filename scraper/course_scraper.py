import re, cgi

from solus_scraper import SolusScraper
from section_scraper import SectionScraper

class CourseScraper(SolusScraper):

    def scrape_current_course(self, subject):
        """Scrapes data for an entire course once its page is open"""

        course = self.solus.current_course(subject)
        course.save(was_scraped=True)

        # Scrape all sections
        SectionScraper(self).scrape_all_sections(course)
