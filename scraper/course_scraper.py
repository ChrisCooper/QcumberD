from solus_scraper import SolusScraper
from section_scraper import SectionScraper


class CourseScraper(SolusScraper):

    def scrape_current_course(self, subject):
        """Scrapes data for an entire course once its page is open"""

        course = self.solus.current_course(subject)

        print ("------Scraping course: {0} - {1}".format(course.number,
               course.title.encode('ascii', 'ignore')))

        course.save(was_scraped=True)

        # Scrape all sections
        SectionScraper(self).scrape_all_sections(course)

        return
