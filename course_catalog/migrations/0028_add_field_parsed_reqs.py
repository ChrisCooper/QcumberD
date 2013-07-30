# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.parsed_reqs'
        db.add_column(u'course_catalog_course', 'parsed_reqs',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Course.parsed_reqs'
        db.delete_column(u'course_catalog_course', 'parsed_reqs')


    models = {
        u'course_catalog.career': {
            'Meta': {'object_name': 'Career'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'course_catalog.consent': {
            'Meta': {'object_name': 'Consent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'course_catalog.course': {
            'Meta': {'object_name': 'Course'},
            'add_consent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_add'", 'null': 'True', 'to': u"orm['course_catalog.Consent']"}),
            'career': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'null': 'True', 'to': u"orm['course_catalog.Career']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'drop_consent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_drop'", 'null': 'True', 'to': u"orm['course_catalog.Consent']"}),
            'enrollment_reqs': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'grading_basis': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'null': 'True', 'to': u"orm['course_catalog.GradingBasis']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'parsed_reqs': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': u"orm['course_catalog.Subject']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'units': ('django.db.models.fields.FloatField', [], {'default': '-1.0'})
        },
        u'course_catalog.courserelation': {
            'Meta': {'object_name': 'CourseRelation'},
            'course': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'course_data'", 'unique': 'True', 'to': u"orm['course_catalog.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'course_catalog.dayofweek': {
            'Meta': {'object_name': 'DayOfWeek'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'course_catalog.gradingbasis': {
            'Meta': {'object_name': 'GradingBasis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'course_catalog.instructor': {
            'Meta': {'object_name': 'Instructor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'course_catalog.requisite': {
            'Meta': {'object_name': 'Requisite'},
            'course_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'for_course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requisites'", 'null': 'True', 'to': u"orm['course_catalog.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'left_index': ('django.db.models.fields.IntegerField', [], {}),
            'right_index': ('django.db.models.fields.IntegerField', [], {}),
            'subject_abbr': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'course_catalog.season': {
            'Meta': {'object_name': 'Season'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'course_catalog.section': {
            'Meta': {'object_name': 'Section'},
            'class_curr': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'class_max': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['course_catalog.Course']"}),
            'date_enrollment_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_in_course': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'null': 'True', 'to': u"orm['course_catalog.Session']"}),
            'solus_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course_catalog.Term']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course_catalog.SectionType']"}),
            'wait_curr': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'wait_max': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        },
        u'course_catalog.sectioncomponent': {
            'Meta': {'object_name': 'SectionComponent'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'section_components'", 'symmetrical': 'False', 'to': u"orm['course_catalog.Instructor']"}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'components'", 'to': u"orm['course_catalog.Section']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'section_components'", 'null': 'True', 'to': u"orm['course_catalog.Timeslot']"})
        },
        u'course_catalog.sectiontype': {
            'Meta': {'object_name': 'SectionType'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'course_catalog.session': {
            'Meta': {'object_name': 'Session'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'course_catalog.subject': {
            'Meta': {'object_name': 'Subject'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'course_catalog.term': {
            'Meta': {'object_name': 'Term'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course_catalog.Season']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'course_catalog.timeslot': {
            'Meta': {'object_name': 'Timeslot'},
            'day_of_week': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course_catalog.DayOfWeek']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_encountered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['course_catalog']