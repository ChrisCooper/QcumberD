# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re, collections
import course_catalog.models
import section_component_helper


def drill_terms_of_sections(course, tools):
    s, config = tools.selen, tools.config
    
    if not s.is_element_present("id=DERIVED_SAA_CRS_SSR_PB_GO"):
        return

    s.click("id=DERIVED_SAA_CRS_SSR_PB_GO")
    tools.wait_for_page()

    #Find terms
    term_options = s.get_select_options("id=DERIVED_SAA_CRS_TERM_ALT")

    #All Terms
    for option in term_options:
        if not len(term_options) == 1:
            s.select("id=DERIVED_SAA_CRS_TERM_ALT", "label=%s" % option)
            s.click("id=DERIVED_SAA_CRS_SSR_PB_GO$92$")
            tools.wait_for_page()
            
        
        #Parse the term and create an object for it if needed
        m = re.search('^([^\s]+) (.*)$', option)
        year =  m.group(1)
        season_name = m.group(2)

        season = course_catalog.models.existing_or_new(course_catalog.models.Season, name=season_name)
        season.save()
            
        term_attributes = {'season' : season,
                           'year' : year}
        term = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attributes)
     
        term.save()

        #Click to view all sections in one page (if there are more pages)
        if s.is_element_present("id=CLASS_TBL_VW5$fviewall$0"):
            s.click("id=CLASS_TBL_VW5$fviewall$0")
            tools.wait_for_page()

        drill_sections(course, term, tools)

def drill_sections(course, term, tools):
    component_rows = component_rows_from_page(tools)
    
    section_component_helper.compile_sections_from_component_rows(component_rows, course, term, tools)
            

def component_rows_from_page(tools):
    """
    Returns the header and component rows for all sections on the page
    """
    s = tools.selen
        
    component_rows = collections.deque()

    index = 1
    locator_format = "xpath=(//td[@class='PSLEVEL2GRIDROW'])[%d]"
    locator = locator_format % index

    rough_row_top = -1000000
    prev_element_left = 1000000
                
    while s.is_element_present(locator):
         
        element_top = s.get_element_position_top(locator)
        element_left = s.get_element_position_left(locator)

        if abs(rough_row_top - element_top) > 5 and element_left < prev_element_left:
            #We're at the next row!
            row = collections.deque()
            component_rows.append(row)

            #Set the standard for this row
            rough_row_top = element_top

        prev_element_left = element_left

        row.append(s.get_text(locator).strip())
            
        index += 1
        locator = locator_format % index
    
    return component_rows