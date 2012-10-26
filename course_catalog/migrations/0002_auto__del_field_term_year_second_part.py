# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Term.year_second_part'
        db.delete_column('course_catalog_term', 'year_second_part')


    def backwards(self, orm):
        
        # Adding field 'Term.year_second_part'
        db.add_column('course_catalog_term', 'year_second_part', self.gf('django.db.models.fields.IntegerField')(default='2013'), keep_default=False)


    models = {
        'course_catalog.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['course_catalog.Subject']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'course_catalog.dayofweek': {
            'Meta': {'object_name': 'DayOfWeek'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'course_catalog.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'course_catalog.season': {
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'course_catalog.section': {
            'Meta': {'object_name': 'Section'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['course_catalog.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_in_course': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'solus_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.Term']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.SectionType']"})
        },
        'course_catalog.sectioncomponent': {
            'Meta': {'object_name': 'SectionComponent'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'section_components'", 'null': 'True', 'to': "orm['course_catalog.Instructor']"}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'components'", 'to': "orm['course_catalog.Section']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'section_components'", 'null': 'True', 'to': "orm['course_catalog.Timeslot']"})
        },
        'course_catalog.sectiontype': {
            'Meta': {'object_name': 'SectionType'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'course_catalog.subject': {
            'Meta': {'object_name': 'Subject'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'course_catalog.term': {
            'Meta': {'object_name': 'Term'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.Season']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'course_catalog.timeslot': {
            'Meta': {'object_name': 'Timeslot'},
            'day_of_week': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['course_catalog.DayOfWeek']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['course_catalog']
