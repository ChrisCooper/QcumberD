from solus_scraper import SolusScraper
from course_scraper import CourseScraper

class SubjectScraper(SolusScraper):

    def scrape_subject(self, subject):
        """Scrapes data for an entire subject once its dropdown is open on the alphanum page"""

        course_index = self.config.course_start_idx

        # Loop through all subject dropdowns by incrementing the link name index
        while self.config.course_end_idx == -1 or course_index < self.config.course_end_idx:

            if self.solus.course_link_exists(course_index):
                self.solus.open_course(course_index)
            else:
                # We've reached the last course
                break
            
            # Scrape everything in the subject
            CourseScraper(self).scrape_current_course(subject)

            self.solus.return_from_course()

            # Advance to the next subject link
            course_index += 1
