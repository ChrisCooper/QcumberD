# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Subject'
        db.create_table('course_catalog_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('course_catalog', ['Subject'])

        # Adding model 'Course'
        db.create_table('course_catalog_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['course_catalog.Subject'])),
        ))
        db.send_create_signal('course_catalog', ['Course'])

        # Adding model 'Section'
        db.create_table('course_catalog_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('solus_id', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('index_in_course', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['course_catalog.Course'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course_catalog.SectionType'])),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course_catalog.Term'])),
        ))
        db.send_create_signal('course_catalog', ['Section'])

        # Adding model 'SectionComponent'
        db.create_table('course_catalog_sectioncomponent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='components', to=orm['course_catalog.Section'])),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='section_components', null=True, to=orm['course_catalog.Instructor'])),
            ('timeslot', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='section_components', null=True, to=orm['course_catalog.Timeslot'])),
        ))
        db.send_create_signal('course_catalog', ['SectionComponent'])

        # Adding model 'SectionType'
        db.create_table('course_catalog_sectiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('course_catalog', ['SectionType'])

        # Adding model 'Instructor'
        db.create_table('course_catalog_instructor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('course_catalog', ['Instructor'])

        # Adding model 'Timeslot'
        db.create_table('course_catalog_timeslot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('day_of_week', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course_catalog.DayOfWeek'])),
        ))
        db.send_create_signal('course_catalog', ['Timeslot'])

        # Adding model 'DayOfWeek'
        db.create_table('course_catalog_dayofweek', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('course_catalog', ['DayOfWeek'])

        # Adding model 'Season'
        db.create_table('course_catalog_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('course_catalog', ['Season'])

        # Adding model 'Term'
        db.create_table('course_catalog_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_encountered', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course_catalog.Season'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('year_second_part', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('course_catalog', ['Term'])


    def backwards(self, orm):
        
        # Deleting model 'Subject'
        db.delete_table('course_catalog_subject')

        # Deleting model 'Course'
        db.delete_table('course_catalog_course')

        # Deleting model 'Section'
        db.delete_table('course_catalog_section')

        # Deleting model 'SectionComponent'
        db.delete_table('course_catalog_sectioncomponent')

        # Deleting model 'SectionType'
        db.delete_table('course_catalog_sectiontype')

        # Deleting model 'Instructor'
        db.delete_table('course_catalog_instructor')

        # Deleting model 'Timeslot'
        db.delete_table('course_catalog_timeslot')

        # Deleting model 'DayOfWeek'
        db.delete_table('course_catalog_dayofweek')

        # Deleting model 'Season'
        db.delete_table('course_catalog_season')

        # Deleting model 'Term'
        db.delete_table('course_catalog_term')


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
            'year': ('django.db.models.fields.IntegerField', [], {}),
            'year_second_part': ('django.db.models.fields.IntegerField', [], {})
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
