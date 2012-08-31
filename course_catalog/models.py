from django.db import models

class ModelOnProbation(models.Model):
    """
    A model that includes a field representing the last time it was encountered during scraping.
    If this item is not encountered during a scraping pass, it should be deleted (since it no longer exists)
    """
    last_encountered = models.DateTimeField()
    
    last_encountered_admin_field_entry = ('Scraping information', {'fields': ['last_encountered'], 'classes': ['collapse']})

class Subject(ModelOnProbation):
    #Attributes
    title = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u"%s - %s" % (self.abbreviation, self.title)


class Course(ModelOnProbation):
    #Attributes
    title = models.CharField(max_length=255)
    description = models.TextField()
    number = models.IntegerField()

    #Relationships
    subject = models.ForeignKey(Subject, related_name='courses')

    def concise_unicode(self):
        return u"%s %s" % (self.subject.abbreviation, self.number)

    def __unicode__(self):
        return u"%s - %s" % (self.concise_unicode(), self.title)

    
class Section(ModelOnProbation):
    #Attributes
    solus_id = models.IntegerField()
    index_in_course = models.IntegerField()

    #Relationships
    course = models.ForeignKey(Course, related_name='sections')
    type = models.ForeignKey("SectionType")
    term = models.ForeignKey("Term")

    def __unicode__(self):
        return u"%s %s (%d) for %s (%d)" % (self.term.__unicode__(), self.type.name, self.index_in_course, self.course.concise_unicode(), self.solus_id)
    

class SectionComponent(ModelOnProbation):
    """
    A date range and instructor/room/timeslot information. A section can be composed of multiple components
    """
    #Attributes
    start_date = models.DateField()
    end_date = models.DateField()
    room = models.CharField(max_length=100)

    #Relationships
    section = models.ForeignKey(Section, related_name="components")
    instructor = models.ForeignKey("Instructor", related_name="section_components")
    timeslot = models.ForeignKey("Timeslot", related_name="section_components")

    def __unicode__(self):
        return u"%s to %s in %s with %s at %s" % (self.start_date.strftime("%A, %B %d, %Y"), self.end_date.strftime("%A, %B %d, %Y"), self.room, self.instructor.name, self.timeslot.__unicode__())


class SectionType(ModelOnProbation):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class Instructor(ModelOnProbation):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Timeslot(ModelOnProbation):
    """
    A slice of time during a particular weekday
    """
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.ForeignKey("DayOfWeek")
    
    def __unicode__(self):
        return u"%s, %s - %s" % (self.day_of_week.abbreviation, self.start_time.strftime("%H:%M%p"), self.end_time.strftime("%H:%M%p"))

class DayOfWeek(models.Model):
    index_in_week = models.IntegerField()
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=3)
    
    def __unicode__(self):
        return self.name

class Season(ModelOnProbation):
    """
    A time of year, such as Fall, or Fall and Winter, that is not specific to a particular year
    """
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class Term(ModelOnProbation):
    """
    A combination of one season and one year (or two, for Fall-Winter courses), exactly specifying a time during which a course is scheduled to be offered
    """
    season = models.ForeignKey(Season)
    year = models.IntegerField()
    year_second_part = models.IntegerField()

    def year_string(self):
        return self.year if self.year == self.year_second_part else u"%d-%d" % (self.year, self.year_second_part)

    def __unicode__(self):
        return u"%s - %s" % (self.season.abbreviation, self.year_string())

