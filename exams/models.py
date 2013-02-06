from django.db import models


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