# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import course_catalog.models
import section_helper, extra_info_helper


def drill_single_course(subject, tools):
    s, config = tools.selen, tools.config

    # Gather the title and description to create a new course
    title, number  = scrape_title(tools)
    description = scrape_description(tools)


    attributes = {'title' : title,
                  'number' : number,
                  'description' : description,
                  'subject' : subject}

    course = course_catalog.models.existing_or_new(course_catalog.models.Course, **attributes)

    # Gather extra info like prerequisites
    extra_info_helper.scrape_extra_info(tools, course)

    course.save()

    section_helper.drill_terms_of_sections(course, tools)

            
def scrape_title(tools):
    s = tools.selen

    raw_title = s.get_text("css=span.PALEVEL0SECONDARY").strip()

    m = re.search('^([\S]+)\s+([\S]+)\s+-\s+(.*)$', raw_title)
        
    subject_abbreviation = m.group(1)
    number = m.group(2)
    title = m.group(3)

    return title, number 

def scrape_description(tools):
    s = tools.selen

    description_locator = "xpath=(//span[@class='PSLONGEDITBOX'])[1]"
    if s.is_element_present(description_locator):
        return s.get_text(description_locator).strip()
    return ""