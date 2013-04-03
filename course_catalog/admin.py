# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from course_catalog.models import *



class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['title', 'abbreviation']}),
    ]
    search_fields = ['abbreviation', 'title']
admin.site.register(Subject, SubjectAdmin)



class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'subject', 'number', 'career', 'grading_basis', 'description', 'units', 'enrollment_reqs', 'add_consent', 'drop_consent']})
    ]
    search_fields = ['title', 'description']
admin.site.register(Course, CourseAdmin)


class RequisiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['left_index', 'right_index', 'subject_abbr', 'course_number', 'for_course']})
    ]
admin.site.register(Requisite, RequisiteAdmin)


class SectionComponentInline(admin.StackedInline):
    model = SectionComponent    
    fieldsets = [
        ('General',     {'fields': ['section', 'instructors', 'room', 'timeslot']}),
        ('Date Span',   {'fields': ['start_date', 'end_date']}),
    ]
    fk_name = 'section'
    extra = 3

class SectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course', 'type', 'term']}),
        ('SOLUS information',               {'fields': ['solus_id', 'index_in_course']}),
    ]
    search_fields = ['title', 'description']
    inlines = [SectionComponentInline]
admin.site.register(Section, SectionAdmin)



class InstructorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    search_fields = ['name']
admin.site.register(Instructor, InstructorAdmin)



class SectionTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'abbreviation', 'order']}),
    ]
admin.site.register(SectionType, SectionTypeAdmin)

class TimeslotAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['day_of_week', 'start_time', 'end_time']}),
    ]
admin.site.register(Timeslot, TimeslotAdmin)


admin.site.register(Term)
admin.site.register(DayOfWeek)
admin.site.register(Season)
admin.site.register(Career)
admin.site.register(Consent)
admin.site.register(GradingBasis)