# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models


class JobConfig(models.Model):
    """
    This class stores a scraping run's configuration, e.g. which subject letters to go through, how long the timeout should be, etc.
    """

    # Non-functional
    name = models.CharField(max_length=255)
    description = models.TextField(default="")

    # Deep scrape?
    deep = models.BooleanField(default=False)

    # Wipe entities that were not encountered in this scrape?
    delete_other_models = models.BooleanField(default=False)

    # Letters to scrape
    letters = models.CharField(max_length=40, default="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    # Subject start/end index
    # Implemented using a list slice
    subject_start_idx = models.IntegerField(default=0)
    subject_end_idx = models.IntegerField(default=-1)
        
    # Subject start/end index
    # Implemented using a list slice
    course_start_idx = models.IntegerField(default=0)
    course_end_idx = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.name

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
