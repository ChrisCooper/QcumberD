# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from course_catalog.models import ModelOnProbation, CourseRelation

class JobConfig(models.Model):
    """
    This class stores a textbook scrap run's configuration
    """

    # Non-functional
    name = models.CharField(max_length=255)
    description = models.TextField(default="")

    # Letters to scrape
    letters = models.CharField(max_length=40, default="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    def __unicode__(self):
        return self.name

class Textbook(ModelOnProbation):
    # Attributes
    title = models.CharField(max_length=256, default="")
    authors = models.CharField(max_length=256, default="", null=True)
    required = models.BooleanField(default=False)
    isbn_10 = models.CharField(max_length=24, default=None, null=True)
    isbn_13 = models.CharField(max_length=24, default=None, null=True)

    # Other info
    new_price = models.CharField(max_length=8, default="")
    new_available = models.IntegerField(default=0)
    used_price = models.CharField(max_length=8, default="")
    used_available = models.IntegerField(default=0)
    classified_info = models.CharField(max_length=128, default="")
    listing_url = models.CharField(max_length=256, default="", null=False);

    # Relationships
    course_rels = models.ManyToManyField("course_catalog.CourseRelation", related_name='textbooks')

    def isbn(self):
        return self.isbn_13 if self.isbn_13 else self.isbn_10
    
    def __unicode__(self):
        return u"%s - %s (%s)" % (self.title, self.authors, self.isbn())
    
    @classmethod
    def existing(cls, **kwargs):
        try:
            return cls.objects.get(title=kwargs['title'],
                                    isbn_10=kwargs['isbn_10'],
                                    isbn_13=kwargs['isbn_13'])
        except ObjectDoesNotExist:
            return None