# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings

class Migration(DataMigration):

    def forwards(self, orm):
        """Change the site name to the one specified in settings"""
        Site = orm['sites.Site']
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = settings.DOMAIN_NAME
        site.name = settings.SITE_NAME
        site.save()

    def backwards(self, orm):
        pass

    complete_apps = ['sites', 'course_catalog']
    symmetrical = True
