import re
import course_catalog.models


def scrape_sections(subject, tools):
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
        term = course = course_catalog.models.existing_or_new(course_catalog.models.Term, **term_attributes)
     
        term.save()
       

