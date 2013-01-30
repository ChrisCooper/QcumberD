# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'JobConfig.delete_other_models'
        db.add_column('scraper_jobconfig', 'delete_other_models',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'JobConfig.delete_other_models'
        db.delete_column('scraper_jobconfig', 'delete_other_models')


    models = {
        'scraper.jobconfig': {
            'Meta': {'object_name': 'JobConfig'},
            'course_end_idx': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'course_start_idx': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deep': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delete_other_models': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letters': ('django.db.models.fields.CharField', [], {'default': "'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'", 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_end_idx': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'subject_start_idx': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['scraper']