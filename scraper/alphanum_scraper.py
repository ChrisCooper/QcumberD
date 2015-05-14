from scraper.solus_scraper import SolusScraper
from scraper.subject_scraper import SubjectScraper

class AlphanumScraper(SolusScraper):

    def scrape_alphanum(self, letter):
        """Scrapes data for an entire alphanum in the course catalog"""
 
        print ("--Scraping letter: " + letter)

        # Go to the page for this letter
        self.solus.select_alphanum(letter)
           
        subject_index = self.config.subject_start_idx

        # Loop through all subject dropdowns by incrementing the link name index
        while self.config.subject_end_idx == -1 or subject_index < self.config.subject_end_idx:

            #Create a subject from the info in the dropdown
            subject = self.solus.subject_from_dropdown(subject_index)

            if not subject:
                # We've reached the end of the subjects
                break

            subject.save(was_scraped=True)

            # Open the subject dropdown
            self.solus.dropdown_subject(subject)
            
            # Scrape everything in the subject
            SubjectScraper(self).scrape_subject(subject)

            # Close the subject dropdown
            self.solus.rollup_subject(subject)

            # Advance to the next subject link
            subject_index += 1
