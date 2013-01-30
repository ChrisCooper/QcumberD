# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SectionType.last_encountered'
        db.delete_column('course_catalog_sectiontype', 'last_encountered')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'SectionType.last_encountered'
        raise RuntimeError("Cannot reverse this migration. 'SectionType.last_encountered' and its values cannot be restored.")

    models = {
        'course_catalog.career': {
            'Meta': {'object_name': 'Career'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
        'course_catalog.dayofweek': {
            'Meta': {'object_name': 'DayOfWeek'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'course_catalog.gradingbasis': {
            'Meta': {'object_name': 'GradingBasis'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'course_catalog.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'course_catalog.season': {
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'course_catalog.section': {
            'Meta': {'object_name': 'Section'},
            'class_curr': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'class_max': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['course_catalog.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_in_course': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'null': 'True', 'to': "orm['course_catalog.Session']"}),
            'solus_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.Term']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.SectionType']"}),
            'wait_curr': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'wait_max': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        },
        'course_catalog.sectioncomponent': {
            'Meta': {'object_name': 'SectionComponent'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'section_components'", 'symmetrical': 'False', 'to': "orm['course_catalog.Instructor']"}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'components'", 'to': "orm['course_catalog.Section']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'section_components'", 'null': 'True', 'to': "orm['course_catalog.Timeslot']"})
        },
        'course_catalog.sectiontype': {
            'Meta': {'object_name': 'SectionType'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'course_catalog.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'course_catalog.subject': {
            'Meta': {'object_name': 'Subject'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'course_catalog.term': {
            'Meta': {'object_name': 'Term'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.Season']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'course_catalog.timeslot': {
            'Meta': {'object_name': 'Timeslot'},
            'day_of_week': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.DayOfWeek']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['course_catalog']