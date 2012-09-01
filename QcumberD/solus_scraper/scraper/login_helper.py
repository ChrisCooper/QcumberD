from django.conf import settings

def navigate_to_course_catalog(d):

    # go to the solus login page
    print "Opening login page..."
    d.get("https://sso.queensu.ca/amserver/UI/Login")

    #Get login information from config file
    with open(settings.SCRAPER_CONFIG_FILE, 'r') as config_file:
        line_num = 0
        login_info = ['','']
        for line in config_file:
            login_info[line_num] = line.strip()
            line_num += 1

    #find login fields
    username_field = d.find_element_by_id("IDToken1")
    password_field = d.find_element_by_id("IDToken2")

    #enter credentials
    username_field.send_keys(login_info[0])
    password_field.send_keys(login_info[1])

    #Log in
    login_button = d.find_element_by_name("Login.Submit")
    login_button.click()

    #Get URL for SOLUS and open it
    solus_link = d.find_element_by_link_text("SOLUS Student Centre")
    solus_url = solus_link.get_attribute("href")
    d.get(solus_url)

    #Get the content frame
    d.switch_to_frame("TargetContent")

    #"Search For Classes"
    search_button = d.find_element_by_id("DERIVED_SSS_SCL_SSS_GO_4$230$")
    search_button.click()

    #"browse course catalog"
    browse_link = d.find_element_by_link_text("browse course catalog")
    browse_link.click()

    print "Navigation to SOLUS course catalog complete."
