import re, cgi

from solus_scraper import SolusScraper
from section_scraper import SectionScraper

class CourseScraper(SolusScraper):

    def scrape_current_course(self, subject):
        """Scrapes data for an entire course once its page is open"""
        
        course = self.solus.current_course(subject)

        course.enrollment_reqs = self.link_requisites(course.enrollment_reqs)

        course.save(was_scraped=True)

        # Scrape all sections
        SectionScraper(self).scrape_all_sections(course)

        return

    def link_requisites(self, s):
        """Inserts links to other courses found in the string"""
        
        # We're displaying this string raw on the site, so we need to escape what er receive first
        s = cgi.escape(s)

        # Find course codes
        matches = re.finditer("([A-Z]{3,4})\s*(\d{3}[AB]?)", s)

        #Because we are replacing strings as we go, the match indecies will become incorrect along the way
        index_offset = 0

        for match in matches:
            repr = '<a href="/search/?q=%s+%s">%s %s</a>' % (match.group(1), match.group(2), match.group(1), match.group(2))

            # Replace the course code with the link representation
            s = s[:match.start() + index_offset] + repr + s[match.end() + index_offset :]

            # Update our ongoing index offset to account for replacement
            index_offset += len(repr) - len(match.group(0))
     
        return s
