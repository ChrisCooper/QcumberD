from django.conf import settings

def navigate_to_course_catalog(tools):
    s = tools.selen

    # go to the solus login page
    print "Opening login page..."
    s.open("https://sso.queensu.ca/amserver/UI/Login")

    #Get login information from config file
    with open(settings.SCRAPER_CONFIG_FILE, 'r') as config_file:
        line_num = 0
        login_info = ['','']
        for line in config_file:
            login_info[line_num] = line.strip()
            line_num += 1

    #type username
    s.type("id=IDToken1", login_info[0])
    #type password
    s.type("id=IDToken2", login_info[1])

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

    print "Navigation to SOLUS course catalog complete."
