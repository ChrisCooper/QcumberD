from django.db import models

from course_catalog.models import *


def largest_sections(term, top_n):
    return Section.objects.all().filter(term=term).order_by('-class_curr')[:top_n]

def largest_winter_sections(top_n):
    winter = Term.objects.all().filter(season__name='Winter', year=2013)
    return largest_sections(winter, top_n)

def pretty_print_section_enrollment(sections):
    for section in sections:
        print('{section.course.subject.abbreviation} {section.course.number} ({section.solus_id}),{section.class_curr},{section.class_max}'.format(section=section))


    winter = Term.objects.all().filter(season__name='Winter', year=2013)
    lecture = SectionType.objects.get(abbreviation="LEC")

def largest_classes(term, section_type, top_n):
    courses = [course_enrolment(c, term, section_type) for c in Course.objects.all()]
    courses = sorted(courses, key=lambda c: (-(c[0] if c[0] else 0), -(c[0] if c[0] else 0)))
    courses.reverse()
    return courses[:top_n]


def course_enrolment(course, term, section_type):
    sections = Section.objects.all().filter(course=course, term=term, type=section_type)
    class_curr = sections.aggregate(Sum('class_curr'))['class_curr__sum']
    class_max = sections.aggregate(Sum('class_max'))['class_max__sum']
    return (class_curr, class_max, course)

def pretty_print_course_enrollment(courses):
    for course in courses:
        print('{course.subject.abbreviation} {course.number},{class_curr},{class_max}'.format(class_curr=c[0], class_max=c[1], course=c[2] ))
