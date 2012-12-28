# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

def navigate_to_course_catalog(tools):
    s = tools.selen

    # go to the solus login page
    print "Opening login page..."
    s.open("https://sso.queensu.ca/amserver/UI/Login")

    #type username
    s.type("id=IDToken1", settings.SCRAPER_USERNAME)
    #type password
    s.type("id=IDToken2", settings.SCRAPER_PASSWORD)

    #Click the log in button
    s.click("name=Login.Submit")

    #Wait for the portal page to load
    tools.wait_for_page()

    #Get URL for SOLUS and open it
    solus_url = s.get_attribute("link=SOLUS Student Centre@href")
    s.open(solus_url)

    #Get the content frame
    s.select_frame("name=TargetContent")

    #"Search For Classes"
    s.click("id=DERIVED_SSS_SCL_SSS_GO_4$230$")

    tools.wait_for_page()

    #"browse course catalog"
    s.click("link=browse course catalog")
    tools.wait_for_page()

    print "Navigation to SOLUS course catalog complete."
