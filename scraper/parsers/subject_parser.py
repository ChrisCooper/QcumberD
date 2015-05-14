import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n

from scraper.parsers.solus_parser import SolusParser

class SubjectParser(SolusParser):
    """Parses the data for a subject dropdown"""

    course_link_id_format = "CRSE_TITLE${0}"

    def course_link_exists(self, course_index):
        """Returns whether or not a course link with the specified index exists"""

        link_id = self.course_link_id(course_index)

        course_link = self.soup.find("a", { "id" : link_id })

        return course_link is not None

    def course_link_id(self, course_index):
        return self.course_link_id_format.format(course_index)
