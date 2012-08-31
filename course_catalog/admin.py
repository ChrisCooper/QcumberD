from django.contrib import admin
from course_catalog.models import *



class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['title', 'abbreviation']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
    search_fields = ['abbreviation', 'title']
admin.site.register(Subject, SubjectAdmin)



class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'subject', 'number', 'description']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
    search_fields = ['title', 'description']
admin.site.register(Course, CourseAdmin)



class SectionComponentInline(admin.StackedInline):
    model = SectionComponent    
    fieldsets = [
        ('General',     {'fields': ['section', 'instructor', 'room', 'timeslot']}),
        ('Date Span',   {'fields': ['start_date', 'end_date']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
    fk_name = 'section'
    extra = 3

class SectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course', 'type', 'term']}),
        ('SOLUS information',               {'fields': ['solus_id', 'index_in_course']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
    search_fields = ['title', 'description']
    inlines = [SectionComponentInline]
admin.site.register(Section, SectionAdmin)



class InstructorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
    search_fields = ['name']
admin.site.register(Instructor, InstructorAdmin)



class NameAbbrAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'abbreviation']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
admin.site.register(SectionType, NameAbbrAdmin)
admin.site.register(Season, NameAbbrAdmin)


class TimeslotAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['day_of_week', 'start_time', 'end_time']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
admin.site.register(Timeslot, TimeslotAdmin)


class TermAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['season', 'year', 'year_second_part']}),
        ModelOnProbation.last_encountered_admin_field_entry,
    ]
admin.site.register(Term, TermAdmin)


admin.site.register(DayOfWeek)