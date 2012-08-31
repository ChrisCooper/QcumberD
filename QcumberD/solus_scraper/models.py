from django.db import models


class JobStatus(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Computer(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class ScrapeJob(models.Model):
    """
    A model that describes a running scrape job on a particular computer.
    """
    time_started = models.DateTimeField()
    time_stopped = models.DateTimeField()
    should_abort = models.BooleanField()
    courses_scraped = models.IntegerField()

    computer = models.ForeignKey(Computer)
    status = models.ForeignKey(JobStatus)

    def __unicode__(self):
        return u'%s: %s, started %s' % (self.computer.name, self.status.name, self.time_started.strftime("%I:%M:%S%p on %A, %B %d, %Y"))

    #News.objects.filter(pk=self.pk).update(last_visited=datetime.datetime.now())