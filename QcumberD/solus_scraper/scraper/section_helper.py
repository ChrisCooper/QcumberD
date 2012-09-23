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
                           'year' : year,
                           'year_second_part' : year}
        term = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attributes)
     
        term.save()

        #Click to view all sections in one page (if there are more pages)
        if s.is_element_present("id=CLASS_TBL_VW5$fviewall$0"):
            s.click("id=CLASS_TBL_VW5$fviewall$0")
            tools.wait_for_page()

        drill_sections(course, term, tools)

def drill_sections(course, term, tools):
    section_pieces = section_pieces_from_page(tools)
        
    while len(section_pieces) > 0:
        section_component_helper.scrape_single_section(section_pieces, course, term, tools)
            

def section_pieces_from_page(tools):
    """
    Returns the header and component rows for all sections on the page
    """
    s = tools.selen
        
    section_pieces = collections.deque()

    index = 1
    locator_format = "xpath=(//td[@class='PSLEVEL2GRIDROW'])[%d]"
    locator = locator_format % index
                
    while s.is_element_present(locator):
            
        section_pieces.append(s.get_text(locator).strip())
            
        index += 1
        locator = locator_format % index
    
    return section_pieces