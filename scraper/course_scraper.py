from solus_scraper import SolusScraper

class CourseScraper(SolusScraper):

    def scrape_current_course(self, subject):
        """Scrapes data for an entire course once its page is open"""

        course = self.solus.current_course(subject)

        course.was_scraped()
        course.save()

        return