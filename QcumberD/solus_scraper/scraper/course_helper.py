def scrape_single_course(tools):
    d, config = tools.driver, tools.config

    #Scrape info from course
    return
    try:
        self.scrape_single_course()
                
        self.course.clean()
                
        self.add_course(self.course)
                
        self.merge_course_if_fullyear()
                
    except SolusModels.UselessCourseException as e:
        print "Ignored"
        SolusModels.SolusCourse.num_courses -= 1
            
        
            
        

