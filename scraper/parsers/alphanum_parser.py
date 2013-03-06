import re

import course_catalog.models as cc
from course_catalog.models import existing_or_new as e_or_n

from solus_parser import SolusParser

class AlphanumParser(SolusParser):
    """Parses the data on alphanum pages"""

    subject_link_name_format = "DERIVED_SSS_BCC_GROUP_BOX_1$84$${0}"

    def subject_from_dropdown(self, subject_index):
        """Returns the subject on the dropdown with name "link_name" on the current alphanum's page, or none if the dropdown does not exist"""

        link_name = self._subject_link_name(subject_index)

        dropdown_link = self.soup.find("a", { "name" : link_name })

        if not dropdown_link:
            # Doesn't exist
            return None

        # Extract the subject title and abbreviation
        m = re.search("^([^-]*) - (.*)$", dropdown_link.get_text().strip())
        subject_abbr = m.group(1)
        subject_title = m.group(2)

        subject = e_or_n(cc.Subject, title=subject_title, abbreviation=subject_abbr)

        # Store the link name so we can click on it later
        subject.click_action = link_name

        return subject


    def _subject_link_name(self, subject_index):
        """The HTML name of the subject dropdown link with the specified index on the current alphanum's page"""
        return self.subject_link_name_format.format(subject_index)
