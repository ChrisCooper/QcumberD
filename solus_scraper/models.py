# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models


class ScrapeJob(models.Model):
    """
    A model that describes a running scrape job on a particular computer.
    """
    time_started = models.DateTimeField()
    time_stopped = models.DateTimeField()
    should_abort = models.BooleanField()
    courses_scraped = models.IntegerField()

    computer = models.ForeignKey('Computer')
    status = models.ForeignKey('JobStatus')
    config = models.ForeignKey('JobConfig')

    

    def __unicode__(self):
        return u'%s on %s: %s, started %s' % (self.config.name, self.computer.name, self.status.name, self.time_started.strftime("%I:%M:%S%p on %A, %B %d, %Y"))


class JobStatus(models.Model):
    REQUESTED = 'requested'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    ERROR = 'error'
    JOB_STATUS_CHOICES = (
        (REQUESTED, 'requested'),
        (STARTED, 'started'),
        (COMPLETED, 'completed'),
        (CANCELLED, 'cancelled'),
        (ERROR, 'error'),
    )
    name = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default=REQUESTED)

    def __unicode__(self):
        return self.name

class Computer(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class JobConfig(models.Model):
    """
    This class stores a scraping run's configuration, e.g. which subject letters to go through, how long the timeout should be, etc.
    """
    name = models.CharField(max_length=255)

    description = models.TextField(default="")

    timeout_milliseconds = models.IntegerField(default=30000)
    
    #While letters of the alphabet the job should scrape the subjects of
    subject_letters = models.CharField(max_length=40)


    #Optional cap for number of subjects per letter to scrape
    #Set to 0 to have no cap
    max_subjects_per_letter = models.IntegerField(default=0)
        
    #The index of the subject to start at in a given alphanum
    starting_subject_index = models.IntegerField(default=0)
        
    #Optional cap for number of courses per subject to scrape
    #Set to 0 to have no cap
    max_courses_per_subject = models.IntegerField(default=0)
        
    #Which index of courses to start at in a given subject
    starting_course_index = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    #News.objects.filter(pk=self.pk).update(last_visited=datetime.datetime.now())



section_types = {
    "BLN": "Blended",
    "CLN": "Clinical",
    #"  ": "Composition"
    "COR": "Correspondence",
    "DIS": "Discussion",
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
    "LTU": "Lecture / Tutorial",
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

weekdays = {
    "Su" : "Sunday",
    "Mo" : "Monday",
    "Tu" : "Tuesday",
    "We" : "Wednesday",
    "Th" : "Thursday",
    "Fr" : "Friday",
    "Sa" : "Saturday",
}