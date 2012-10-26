# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'JobConfig.description'
        db.add_column('solus_scraper_jobconfig', 'description', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'JobConfig.description'
        db.delete_column('solus_scraper_jobconfig', 'description')


    models = {
        'solus_scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'solus_scraper.jobconfig': {
            'Meta': {'object_name': 'JobConfig'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_courses_per_subject': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_subjects_per_letter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'starting_course_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'starting_subject_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject_letters': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'timeout_milliseconds': ('django.db.models.fields.IntegerField', [], {})
        },
        'solus_scraper.jobstatus': {
            'Meta': {'object_name': 'JobStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'requested'", 'max_length': '20'})
        },
        'solus_scraper.scrapejob': {
            'Meta': {'object_name': 'ScrapeJob'},
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solus_scraper.Computer']"}),
            'config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solus_scraper.JobConfig']"}),
            'courses_scraped': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'should_abort': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['solus_scraper.JobStatus']"}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {}),
            'time_stopped': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['solus_scraper']
