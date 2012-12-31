from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD
from solus_scraper import SolusScraper

def scrape_enrollment(config, section):
    """
    Scrapes the enrollment information of a section
    Returns a (capacity, enrolled) tuple
    """
    # Deprecated by scrape_section()

    s = SolusSession(SCRAPER_USERNAME, SCRAPER_PASSWORD)
    term = section.term
    course = section.course
    subject = course.subject
    
    s.select_alphanum(subject.abbreviation[:1])
    s.dropdown_subject(subject.abbreviation, subject.title)
    s.select_course(course.number)
    s.show_sections()
    s.switch_terms(term.year, term.season)
    s.show_all_sections()
    s.view_section(section.solus_id)

    capacity, enrolled = s.parser().enrollment_stats()

    s.return_from_section()
    s.return_from_course()

    s.close_session()
    
    return capacity, enrolled

def test_request():
    """Return what should be displayed (html or otherwise)"""

    try:
        SolusScraper(None, SCRAPER_USERNAME, SCRAPER_PASSWORD).full_scrape()
        return "<html>Finished scraping!</html>"
    except Exception as e:
        #return "<html>Error encoutered!<br/><br/>" + str(e) + "</html>"
        raise e
