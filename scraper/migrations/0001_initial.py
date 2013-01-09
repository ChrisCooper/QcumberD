# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JobConfig'
        db.create_table('scraper_jobconfig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('deep', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('letters', self.gf('django.db.models.fields.CharField')(default='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', max_length=40)),
            ('subject_start_idx', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('subject_end_idx', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('course_start_idx', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('course_end_idx', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal('scraper', ['JobConfig'])


    def backwards(self, orm):
        # Deleting model 'JobConfig'
        db.delete_table('scraper_jobconfig')


    models = {
        'scraper.jobconfig': {
            'Meta': {'object_name': 'JobConfig'},
            'course_end_idx': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'course_start_idx': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deep': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letters': ('django.db.models.fields.CharField', [], {'default': "'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'", 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_end_idx': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'subject_start_idx': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['scraper']