import course_catalog.models
from decimal import Decimal


def scrape_extra_info(tools, course):

    titles = []
    title_locator_formats = ["xpath=(//label[@class='PSDROPDOWNLABEL'])[%d]", "xpath=(//label[@class='PSEDITBOXLABEL'])[%d]"]
    
    values = []
    value_locator_formats = ["xpath=(//span[@class='PSDROPDOWNLIST_DISPONLY'])[%d]","xpath=(//span[@class='PSEDITBOX_DISPONLY'])[%d]"]
    
    for format in title_locator_formats:
        add_entries_for_position(tools, titles, format)
    
    
    for format in value_locator_formats:
        add_entries_for_position(tools, values, format)
    
    
    info_mappings = {}
    
    #Match values to titles
    for (value_text, value_pos_x, value_pos_y) in values:
        
        best_diff = 10000
        best_text = None
        for (title_text, title_pos_x, title_pos_y) in titles:
            diff = abs(title_pos_y - value_pos_y)
            if value_pos_y > title_pos_y - 5 and diff < best_diff:
                best_diff = diff
                best_text = title_text
            
        #Add the value to the info mapping for that title
        if best_text:
            if best_text == "Course Components":
                #Add both the value and the vertical position, for matching values later
                if best_text in info_mappings:
                    info_mappings[best_text].append((value_text, value_pos_x, value_pos_y))
                else:
                    info_mappings[best_text] = [(value_text, value_pos_x, value_pos_y)]
            else:
                if best_text in info_mappings:
                    info_mappings[best_text] += " " + value_text
                else:
                    info_mappings[best_text] = value_text
        else:
            print "No match for %s" % value_text
    
    final_components = {}
    
    
    
    if "Course Components" in info_mappings:
        components = info_mappings["Course Components"]
        
        for (component_text, component_pos_x, component_pos_y) in components:
        
            best_diff = 10000
            best_text = None
            
            for (value_text, value_pos_x, value_pos_y) in components:
                
                #Make sure it's only added once
                if component_pos_x >= value_pos_x - 10:
                    continue
                
                diff = abs(component_pos_y - value_pos_y)
                if diff < best_diff:
                    best_diff = diff
                    best_text = value_text
            
            if best_text:
                final_components[component_text] = value_text
    
    info_mappings["Course Components"] = final_components

    assign_extra_values_to_course(tools, info_mappings, course)

            
def add_entries_for_position(tools, entries, locator_format_string):
    s = tools.selen

    index = 1
    locator = locator_format_string % index
    while s.is_element_present(locator):
        entries.append((s.get_text(locator).strip(), s.get_element_position_left(locator), s.get_element_position_top(locator)))
                
        index += 1
        locator = locator_format_string % index


def assign_extra_values_to_course(tools, info, course):

    info = [(tools.extra_info_mappings[key], value) for key, value in info.iteritems()]

    for key, value in info:

        if key == "career":
            attributes = {"name": value}
            course.career = course_catalog.models.existing_or_new(course_catalog.models.Career, **attributes)
            pass

        elif key == "units":
            if len(value.split(".")[1]) > 2:
                raise Exception('Error: assumption about precision or magnitude of credit hours (units) is false: "%s"' % value)
            course.units = float(value)

        elif key == "grading_basis":
            pass
        elif key == "add_consent":
            pass
        elif key == "course_componenets":
            pass
        elif key == "drop_consent":
            pass
        elif key == "enrollment_requirement":
            course.enrollment_reqs = value
            pass
        elif key == "typically_offered":
            pass
        else:
            raise Exception('Unknown extra info type: "%s"' % value)
            #setattr(course, key, value)





