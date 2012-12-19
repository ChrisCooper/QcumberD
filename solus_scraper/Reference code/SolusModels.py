# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

info_mappings_simple_keys = {"Career": "career",
                             "Units": "units",
                             "Grading Basis": "grading_basis",
                             "Add Consent": "add_consent",
                             "Course Components": "course_componenets",
                             "Drop Consent": "drop_consent",
                             "Enrollment Requirement": "enrollment_requirement",
                             }
info_mappings_json_keys = {"units": "u",
                           "grading_basis": "g",
                           "add_consent": "ac",
                           "course_componenets": "c",
                           "drop_consent": "dc",
                           "enrollment_requirement": "e",
                           }


class SolusCourse:
    
    num_courses = 0
    
    def __init__(self, course_dict=None):
        
        self.duplicate_suffix = ""
        
        #Check for construction from dictionary
        if course_dict:
            self.title = course_dict["t"]
            self.num = course_dict["n"]
            self.description = course_dict["d"]
            
            self.subject = course_dict["s"]
            self.sections = []
            for section_dict in course_dict["sec"]:
                self.sections.append(Section(section_dict))
                
            #info_mappings
            for variable, json in info_mappings_json_keys.iteritems():
                if json in course_dict:
                    setattr(self, variable, course_dict[json])
            
            
            return
        
        self.title = ""
        self.num = ""
        self.description = ""
        
        self.subject = ""
        self.sections = []
        
        #info_mappings
        for human, variable_name in info_mappings_simple_keys.iteritems():
            setattr(self, variable_name, "")
        
        #for debugging
        self.subject_description = ""
    
    
    def move_aside(self):
        self.duplicate_suffix += " duplicate"
        
    def add_merged_info(self, first, second):
        self.title = first.title
        self.num = first.num[:-1]
        self.description = first.description
        
        self.subject = first.subject
        self.sections = []
        
        #Merge the individual sections
        for s1 in first.sections:
            for s2 in second.sections:
                if s1.index == s2.index:
                    s1.id += ",%s" % s2.id
                    
                    term = term_by_combination(Term.terms[s1.term], Term.terms[s2.term])
                    s1.term = term_index_by_key(term.get_key())

                    s1.components += s2.components
                    self.sections.append(s1)
                    break
    
    def get_key(self):
        return "%s %s%s" % (self.subject, self.num, self.duplicate_suffix)
    
    def clean(self):
        for section in self.sections:
            section.clean()
    
    def describe(self):
        print u"\n\nCourse:\n(%s/%s %s) %s" % (self.subject_description, self.subject, self.num, self.title)
        print self.description
        for section in self.sections:
            section.describe()
        
        #info mappings
        for human, variable in info_mappings_simple_keys.iteritems():
            val = getattr(self, variable)
            if val:
                print "%s: %s" % (human, val)
    
    def jsonable(self):
        d = {}
        d["t"] = self.title
        d["n"] = self.num
        d["d"] = self.description
        
        d["s"] = self.subject
        d["sec"] = [section.jsonable() for section in self.sections]
        
        #info_mappings
        for variable, json in info_mappings_json_keys.iteritems():
            val = getattr(self, variable)
            if val:
                d[json] = val
        
        return d




class Section:
    def __init__(self, section_dict=None):
        if section_dict:
            self.index = section_dict["in"]
            self.id = section_dict["id"]
            
            self.term = section_dict["te"]
            self.type = section_dict["ty"]
            self.components = []
            for component_dict in section_dict["c"]:
                self.components.append(SecionComponent(component_dict))
            return
            
        self.index = ""
        self.id = ""
        
        self.type = ""
        self.term = ""
        self.components = []
    
    def clean(self):
        for component in self.components:
            component.clean()
    
    def describe(self):
        print u"\nSection:\n(%s) %s-%s, Term: %s" % (self.id, self.type, self.index, self.term)
        for component in self.components:
            component.describe()
    
    def jsonable(self):
        d = {}
        d["in"] = self.index
        d["id"] = self.id
        
        d["te"] = self.term
        d["ty"] = self.type
        d["c"] = [component.jsonable() for component in self.components]
        return d

class SectionComponent:
    def __init__(self, section_component_dict=None):
        if section_component_dict:
            self.room = time_dict["r"]
            self.instructor = time_dict["i"]
            self.start_date = time_dict["sd"]
            self.end_date = time_dict["ed"]
            self.timeslot = time_dict["ts"]
            return
        
        self.start_date = ""
        self.end_date = ""
        self.room = ""
        self.instructor = ""
        self.timeslot = ""
    
    def clean(self):
        self.instructor = self.instructor.replace(" \n ", " ")
    
    def describe(self):
        print u"%s-%s in %s, with %s. %s" % (self.start_date, self.end_date, self.room, self.instructor, self.timeslot)
    
    def jsonable(self):
        d = {}
        
        d["sd"] = self.start_date
        d["ed"] = self.end_date
        d["r"] = self.room
        d["i"] = self.instructor
        d["ts"] = self.timeslot
        return d

def timeslot_index_by_components(day, start, end):
    index = 0
    
    key = "%s, %s-%s" % (day, start, end)
    
    for timeslot in Timeslot.timeslots:
        if timeslot.get_key() == key:
            return index
        index += 1
    
    timeslot = Timeslot()
    Timeslot.timeslots.append(timeslot)
    
    timeslot.day =  day
    timeslot.start = start
    timeslot.end = end
    
    return index

def timeslot_index_by_key(key):
    index = 0
    for timeslot in Timeslot.timeslots:
        if timeslot.get_key() == key:
            return index
        index += 1
    
    timeslot = Timeslot()
    Timeslot.timeslots.append(timeslot)
    
    m = re.search('^(.*), (.*)-(.*)$', key)
    timeslot.day =  m.group(1)
    timeslot.start =  m.group(1)
    timeslot.end =  m.group(1)
    
    return index

class Timeslot:
    timeslots = []
    
    def __init__(self, time_dict=None):
        if time_dict:
            self.day = time_dict["d"]
            self.start = time_dict["s"]
            self.end = time_dict["e"]
            return
        
        self.day = ""
        self.start = ""
        self.end = ""
    
    def get_key(self):
        return "%s, %s-%s" % (self.day, self.start, self.end)
    
    def describe(self):
        print u"%s, %s-%s" % (self.day, self.start, self.end)
    
    def jsonable(self):
        d = {}
        d["d"] = self.day
        d["s"] = self.start
        d["e"] = self.end
        return d

def term_by_combination(t1, t2):
    term = Term()
    term.season = "Fall and Winter"
    years = [t1.year, t2.year]
    years.sort()
    term.year = "%s-%s" % (years[0], years[1])
    return term
    
def term_index_by_key(key):
    index = 0
    for term in Term.terms:
        if term.get_key() == key:
            return index
        index += 1
    
    term = Term()
    Term.terms.append(term)
    
    m = re.search('^([^\s]+) (.*)$', key)
    term.year =  m.group(1)
    term.season =  m.group(2)
    
    return index

class Term:
    terms = []
    
    def __init__(self, term_dict=None):
        if term_dict:
            self.season = term_dict["s"]
            self.year = term_dict["y"]
            return
        
        self.season = ""
        self.year = ""
    
    def get_key(self):
        return "%s %s" % (self.year, self.season)
    
    def jsonable(self):
        d = {}
        d["s"] = self.season
        d["y"] = self.year
        return d

def subject_index_by_key(key, title=""):
    index = 0
    for subject in Subject.subjects:
        if subject.get_key() == key:
            return index
        index += 1
    
    subject = Subject()
    Subject.subjects.append(subject)
    
    subject.abbr = key
    subject.title = title
    
    return index

class Subject:
    subjects = []
    
    def __init__(self, subject_dict=None):
        if subject_dict:
            self.abbr = subject_dict["a"]
            self.title = subject_dict["t"]
            return
        
        self.abbr = ""
        self.title = ""
    
    def get_key(self):
        return self.abbr
    
    def jsonable(self):
        d = {}
        d["a"] = self.abbr
        d["t"] = self.title
        return d

def section_type_index_by_key(key):
    index = 0
    for section_type in SectionType.section_types:
        if section_type.get_key() == key:
            return index
        index += 1
    
    section_type = SectionType()
    SectionType.section_types.append(section_type)
    
    section_type.abbr = key
    if key in section_types:
        section_type.name = section_types[key]
    else:
        section_type.name = key
    
    return index

section_types = {
    "CLN": "Clinical",
    #"  ": "Composition"
    "COR": "Correspondence",
    #"  ": "Discussion",
    #"  ": "Discussion / Laboratory",
    #"  ": "Ensemble",
    "EXM": "Exam",
    "FLD": "Field Studies",
    "IND": "Individual Study",
    "LAB": "Laboratory",
    #"  ": "Laboratory / Conversation",
    #"  ": "Laboratory / Seminar",
    #"  ": "Laboratory / Tutorial",
    "LEC": "Lecture",
    #"  ": "Laboratory / Demonstration",
    "LDI": "Lecture / Discussion",
    "LLB": "Lecture / Laboratory",
    "LSM": "Lecture / Seminar",
    #"  ": "Lecture / Tutorial",
    #"  ": "Meeting",
    #"  ": "Oral",
    #"  ": "Oral / Conversation",
    "PRA": "Practicum",
    "PRJ": "Project",
    "REA": "Reading",
    "RSC": "Research",
    "SEM": "Seminar",
    #"  ": "Seminar / Discussion",
    #"  ": "Seminar / Workshop",
    #"  ": "Speaker",
    "STD": "Studio",
    #"  ": "Technical Workshop",
    "THE": "Thesis Research",
    "TUT": "Tutorial",
    #"  ": "Unknown",
    #"  ": "Workshop",
    }

class SectionType:
    section_types = []
    
    def __init__(self, section_type_dict=None):
        if section_type_dict:
            self.abbr = subject_dict["a"]
            self.name = subject_dict["n"]
            return
        
        self.abbr = ""
        self.name = ""
    
    def get_key(self):
        return self.abbr
    
    def jsonable(self):
        d = {}
        d["a"] = self.abbr
        d["n"] = self.name
        return d

days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su", "TB"]

def index_of_day_abbr(abbr):
    return days.index(abbr)

class UselessCourseException(Exception):
    def __init__(self, course_code):
        self.course_code = course_code
    def __str__(self):
        return repr(self.course_code)