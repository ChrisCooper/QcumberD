# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CourseRelation'
        db.delete_table('textbooks_courserelation')


    def backwards(self, orm):
        # Adding model 'CourseRelation'
        db.create_table('textbooks_courserelation', (
            ('course', self.gf('django.db.models.fields.related.OneToOneField')(related_name='course_data', unique=True, to=orm['course_catalog.Course'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('textbooks', ['CourseRelation'])


    models = {
        'course_catalog.career': {
            'Meta': {'object_name': 'Career'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'course_catalog.consent': {
            'Meta': {'object_name': 'Consent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'course_catalog.course': {
            'Meta': {'object_name': 'Course'},
            'add_consent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_add'", 'null': 'True', 'to': "orm['course_catalog.Consent']"}),
            'career': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'null': 'True', 'to': "orm['course_catalog.Career']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'drop_consent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_drop'", 'null': 'True', 'to': "orm['course_catalog.Consent']"}),
            'enrollment_reqs': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'grading_basis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'null': 'True', 'to': "orm['course_catalog.GradingBasis']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['course_catalog.Subject']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'units': ('django.db.models.fields.FloatField', [], {'default': '-1.0'})
        },
        'course_catalog.courserelation': {
            'Meta': {'object_name': 'CourseRelation'},
            'course': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'course_data'", 'unique': 'True', 'to': "orm['course_catalog.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'course_catalog.gradingbasis': {
            'Meta': {'object_name': 'GradingBasis'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'course_catalog.subject': {
            'Meta': {'object_name': 'Subject'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'textbooks.jobconfig': {
            'Meta': {'object_name': 'JobConfig'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letters': ('django.db.models.fields.CharField', [], {'default': "'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'", 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'textbooks.textbook': {
            'Meta': {'object_name': 'Textbook'},
            'authors': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True'}),
            'classified_info': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'course_rels': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'textbooks'", 'symmetrical': 'False', 'to': "orm['course_catalog.CourseRelation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '24', 'null': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '24', 'null': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'listing_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'new_available': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_price': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'used_available': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'used_price': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8'})
        }
    }

    complete_apps = ['textbooks']