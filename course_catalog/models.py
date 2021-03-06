# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from datetime import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class ModelOnProbation(models.Model):
    """An abstract model that includes a field representing the last time it
    was encountered during scraping.
    If this item is not encountered during a scraping pass, it should be
    deleted (since it no longer exists).
    """
    last_encountered = models.DateTimeField(auto_now_add=True)

    last_encountered_admin_field_entry = ('Scraping information',
                                          {'fields': ['last_encountered'],
                                          'classes': ['collapse']})

    class Meta:
        abstract = True

    def was_scraped(self):
        """Resets the "last_encountered" field to the current time"""
        self.last_encountered = datetime.now()

    def save(self, *args, **kwargs):
        if "was_scraped" in kwargs:
            self.was_scraped()
            del kwargs["was_scraped"]

        super(ModelOnProbation, self).save(*args, **kwargs)


class Subject(ModelOnProbation):
    #Attributes
    title = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10, db_index=True)

    def __unicode__(self):
        return u"{self.abbreviation} - {self.title}".format(self=self)

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(abbreviation=kwargs['abbreviation'])
        except ObjectDoesNotExist:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('course_catalog.views.subject_detail', (),
                {'subject_abbr': self.abbreviation})


class Course(ModelOnProbation):
    #Attributes
    title = models.CharField(max_length=255)
    description = models.TextField()
    number = models.CharField(max_length=10, db_index=True)
    units = models.FloatField(default=-1.)
    enrollment_reqs = models.TextField(default="")

    #Relationships
    subject = models.ForeignKey(Subject, related_name='courses')
    career = models.ForeignKey("Career", related_name='courses', null=True)
    grading_basis = models.ForeignKey("GradingBasis", related_name='courses',
                                      null=True)
    add_consent = models.ForeignKey("Consent", related_name='courses_add',
                                    null=True)
    drop_consent = models.ForeignKey("Consent", related_name='courses_drop',
                                     null=True)

    @property
    def is_empty(self):
        return self.sections.count() == 0

    @property
    def seasons_offered(self):
        return set([s.term.season for s in self.sections.all()])

    def concise_unicode(self):
        return u"{self.subject.abbreviation} {self.number}".format(self=self)

    def __unicode__(self):
        return u"{concise} - {title}".format(
            concise=self.concise_unicode(), title=self.title)

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(subject=kwargs['subject'],
                                   number=kwargs['number'])
        except ObjectDoesNotExist:
            return None

    def link_requisites(self):
        """Insert links into the requisites text.

        Note that this method assumes that self.requisites.all() returns reqs
        in the same order that they appear in the text!
        """
        text = self.enrollment_reqs
        reqs = self.requisites.all().order_by('left_index')
        offset = 0
        for req in reqs:
            left = text[:req.left_index + offset]
            right = text[req.right_index + offset:]
            course = req.req_exists()
            if course:
                extra = u'title="{}" class="requisite"'.format(course.title)
            else:
                extra = u'title="This course cannot be found on Solus" class="missing requisite"'
            url = course.get_absolute_url() if course else u"/catalog/{subj}/{num}"\
                .format(subj=req.subject_abbr, num=req.course_number)
            link = u'<a href="{url}" {extra}>{abbr} {num}</a>'.format(url=url, abbr=req.subject_abbr, num=req.course_number, extra=extra)
            offset += len(link) - (req.right_index - req.left_index)
            text = left + link + right
        return text

    @models.permalink
    def get_absolute_url(self):
        return ('course_catalog.views.course_detail', (), {
                'subject_abbr': self.subject.abbreviation,
                'course_number': self.number})


class Requisite(ModelOnProbation):
    """Enrollment requisites come from a free-form text field on solus. That
    field is parsed to find the actual course. Some of them exist. Instances of
    this model describe where in the text string those courses occur, and
    provide helper methods to work with them.
    """
    subject_abbr = models.CharField(max_length=10)
    course_number = models.CharField(max_length=10)
    left_index = models.IntegerField()
    right_index = models.IntegerField()
    #exists = models.BooleanField(default=False)

    for_course = models.ForeignKey("Course", related_name='requisites',
                                   null=True)

    def __unicode__(self):
        return u'{coursename}: {self.subject_abbr} {self.course_number}'.format(
            coursename=self.for_course.concise_unicode(), self=self)

    @classmethod
    def existing(cls, **properties):
        try:
            return cls.objects.get(**properties)
        except ObjectDoesNotExist:
            return None

    def req_exists(self):
        c = Course.objects.filter(subject__abbreviation__iexact=self.subject_abbr, number__istartswith=self.course_number).order_by('number')
        return c[0] if len(c) > 0 else None


class Section(ModelOnProbation):
    #Attributes
    solus_id = models.CharField(max_length=16)
    index_in_course = models.CharField(max_length=8)

    # From a deep scrape
    class_curr = models.IntegerField(default=-1)
    class_max = models.IntegerField(default=-1)
    wait_curr = models.IntegerField(default=-1)
    wait_max = models.IntegerField(default=-1)
    date_enrollment_updated = models.DateTimeField(default=datetime.now)

    #Relationships
    course = models.ForeignKey("Course", related_name='sections')
    type = models.ForeignKey("SectionType")
    term = models.ForeignKey("Term")

    # From a deep scrape
    session = models.ForeignKey("Session", related_name='sections', null=True)

    def __unicode__(self):
        return u"{t} {s.type.name} ({s.index_in_course}) for {c} ({s.solus_id})"\
            .format(s=self, t=self.term.__unicode__(),
                    c=self.course.concise_unicode())

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(index_in_course=kwargs['index_in_course'],
                                   solus_id=kwargs['solus_id'],
                                   course=kwargs['course'],
                                   term=kwargs['term'])
        except ObjectDoesNotExist:
            return None

    def enrollment_was_scraped(self):
        """Resets the "date_enrollment_updated" field to the current time"""
        self.date_enrollment_updated = datetime.now()


class SectionComponent(ModelOnProbation):
    """A date range and instructor/room/timeslot information. A section can be
    composed of multiple components.
    """
    #Attributes
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)

    #Relationships
    section = models.ForeignKey(Section, related_name="components")
    instructors = models.ManyToManyField("Instructor",
                                         related_name="section_components")
    timeslot = models.ForeignKey("Timeslot", related_name="section_components",
                                 blank=True, null=True)

    def __unicode__(self):
        return u"{start} to {end} in {s.room} with {prof} at {s.timeslot}"\
            .format(s=self, start=self.start_date.strftime("%A, %B %d, %Y"),
                    end=self.end_date.strftime("%A, %B %d, %Y"),
                    prof=self.instructors_string())

    def instructors_string(self):
        return ", ".join(i.name for i in self.instructors.all())

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(start_date=kwargs['start_date'],
                                   end_date=kwargs['end_date'],
                                   section=kwargs['section'],
                                   timeslot=kwargs['timeslot'],)
        except ObjectDoesNotExist:
            return None


class Timeslot(ModelOnProbation):
    """A slice of time during a particular weekday."""
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.ForeignKey("DayOfWeek")

    def __unicode__(self):
        return u"{day}, {start} - {end}".format(
            day=self.day_of_week.abbreviation,
            start=self.start_time.strftime("%I:%M%p"),
            end=self.end_time.strftime("%I:%M%p"))

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(start_time=kwargs['start_time'],
                                   end_time=kwargs['end_time'],
                                   day_of_week=kwargs['day_of_week'])
        except ObjectDoesNotExist:
            return None


class Season(ModelOnProbation):
    """A time of year, such as Fall, or Fall and Winter, that is not specific
    to a particular year
    """
    name = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(name=kwargs['name'])
        except ObjectDoesNotExist:
            return None


class Term(ModelOnProbation):
    """A combination of one season and one year (or two, for Fall-Winter
    courses), exactly specifying a time during which a course is scheduled to
    be offered.
    """
    season = models.ForeignKey(Season)
    year = models.IntegerField()
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return u"{self.season.name} - {self.year}".format(self=self)

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(season=kwargs['season'], year=kwargs['year'])
        except ObjectDoesNotExist:
            return None


class CourseRelation(ModelOnProbation):
    """Holds extra information about a course"""

    # Relationships
    course = models.OneToOneField("course_catalog.Course",
                                  related_name='course_data', null=False)

    def __unicode__(self):
        return u"Data attached to {self.course}".format(self=self)

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(course=kwargs['course'])
        except ObjectDoesNotExist:
            return None


class StringModel(ModelOnProbation):
    """Serves as a base class for models which only contain one string called
    "name".
    """

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(name=kwargs['name'])
        except ObjectDoesNotExist:
            return None


class Instructor(StringModel):
    name = models.CharField(max_length=100)


class Session(StringModel):
    name = models.CharField(max_length=50)


class Consent(StringModel):
    """E.g. 'Department Consent Required'."""
    name = models.CharField(max_length=50)


def existing_or_new(model, **kwargs):

    #get the object with the specified attributes
    existing = model.existing(**kwargs)
    if existing is None:
        existing = model(**kwargs)
        existing.save()
    else:
        # We need to make sure the extra attributes are updated
        for key, val in kwargs.iteritems():
            setattr(existing, key, val)
        existing.save()
    return existing


# Fixtures ---------------------------------------------

class Career(models.Model):
    """A course classification, such as 'Undergraduate'."""
    name = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(name=kwargs['name'])
        except ObjectDoesNotExist:
            return None


class DayOfWeek(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=3)

    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(abbreviation=kwargs['abbreviation'])
        except ObjectDoesNotExist:
            return None


class SectionType(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(abbreviation=kwargs['abbreviation'])
        except ObjectDoesNotExist:
            return None


class GradingBasis(models.Model):
    """E.g. 'Graded'."""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(name=kwargs['name'])
        except ObjectDoesNotExist:
            return None
