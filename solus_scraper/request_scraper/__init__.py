from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD
from solus_session import SolusSession

def full_scrape(config):
    """Starts a full scrape of the SOLUS database"""
    sessions = []

def scrape_enrollment(config, section):
    """Scrapes the enrollment information of a section"""
    """Returns a (capacity, enrolled) tuple"""

    s = SolusSession(SCRAPER_USERNAME, SCRAPER_PASSWORD)
    course = section.course

    s.navigate_to_course(course)
    s.show_sections()
    s.switch_terms(section.term)
    s.show_all_sections()
    s.view_section(section)

    capacity, enrolled = s.parser().enrollment_stats()

    s.return_from_section()
    s.return_from_course()

    s.close_session()
    
    return capacity, enrolled 

scrape_enrollment(None, None)

