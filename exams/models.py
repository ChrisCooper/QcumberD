# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from course_catalog.models import ModelOnProbation, CourseRelation


class JobConfig(models.Model):
    """
    This class stores a exam scraping run's configuration
    """

    # Non-functional
    name = models.CharField(max_length=255)
    description = models.TextField(default="")

    # The years to scrape
    # Implemented using a list slice
    year_start_idx = models.IntegerField(default=0)
    year_end_idx = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.name


class Exam(ModelOnProbation):

    # Attributes
    year = models.CharField(max_length=9, default="", null=True)
    pdf_url = models.CharField(max_length=256, default="", null=False);

    # Relationships
    course_rels = models.ManyToManyField("course_catalog.CourseRelation", related_name='exams')
    
    def __unicode__(self):
        return u"Exam PDF at {0}".format(self.pdf_url)
    
    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(year=kwargs['year'],
                                    pdf_url=kwargs['pdf_url'])
        except ObjectDoesNotExist:
            return None