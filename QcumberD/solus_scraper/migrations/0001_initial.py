# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ScrapeJob'
        db.create_table('solus_scraper_scrapejob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_started', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_stopped', self.gf('django.db.models.fields.DateTimeField')()),
            ('should_abort', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('courses_scraped', self.gf('django.db.models.fields.IntegerField')()),
            ('computer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solus_scraper.Computer'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solus_scraper.JobStatus'])),
            ('config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solus_scraper.JobConfig'])),
        ))
        db.send_create_signal('solus_scraper', ['ScrapeJob'])

        # Adding model 'JobStatus'
        db.create_table('solus_scraper_jobstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='requested', max_length=20)),
        ))
        db.send_create_signal('solus_scraper', ['JobStatus'])

        # Adding model 'Computer'
        db.create_table('solus_scraper_computer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('solus_scraper', ['Computer'])

        # Adding model 'JobConfig'
        db.create_table('solus_scraper_jobconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timeout_milliseconds', self.gf('django.db.models.fields.IntegerField')()),
            ('subject_letters', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('max_subjects_per_letter', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('starting_subject_index', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_courses_per_subject', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('starting_course_index', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('solus_scraper', ['JobConfig'])


    def backwards(self, orm):
        
        # Deleting model 'ScrapeJob'
        db.delete_table('solus_scraper_scrapejob')

        # Deleting model 'JobStatus'
        db.delete_table('solus_scraper_jobstatus')

        # Deleting model 'Computer'
        db.delete_table('solus_scraper_computer')

        # Deleting model 'JobConfig'
        db.delete_table('solus_scraper_jobconfig')


    models = {
        'solus_scraper.computer': {
            'Meta': {'object_name': 'Computer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'solus_scraper.jobconfig': {
            'Meta': {'object_name': 'JobConfig'},
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
