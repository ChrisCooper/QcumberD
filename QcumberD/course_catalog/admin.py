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
        (None, {'fields': ['title', 'subject', 'number', 'description']}),
    ]
    search_fields = ['title', 'description']
admin.site.register(Course, CourseAdmin)



class SectionComponentInline(admin.StackedInline):
    model = SectionComponent    
    fieldsets = [
        ('General',     {'fields': ['section', 'instructor', 'room', 'timeslot']}),
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



class NameAbbrAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'abbreviation']}),
    ]
admin.site.register(SectionType, NameAbbrAdmin)

class TimeslotAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['day_of_week', 'start_time', 'end_time']}),
    ]
admin.site.register(Timeslot, TimeslotAdmin)

class SeasonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
admin.site.register(Season, SeasonAdmin)

class TermAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['season', 'year']}),
    ]
admin.site.register(Term, TermAdmin)


admin.site.register(DayOfWeek)