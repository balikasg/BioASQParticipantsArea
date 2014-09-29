# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Detail1b'
        db.create_table('task1b_detail1b', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phase', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('test_id', self.gf('django.db.models.fields.IntegerField')()),
            ('started', self.gf('django.db.models.fields.DateTimeField')()),
            ('finished', self.gf('django.db.models.fields.DateTimeField')()),
            ('number_of_questions', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('golden_path', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('number_of_downloads', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('downloaders', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_oracle', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('task1b', ['Detail1b'])

        # Adding model 'golden_question_1b'
        db.create_table('task1b_golden_question_1b', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('concepts', self.gf('django.db.models.fields.TextField')()),
            ('documents', self.gf('django.db.models.fields.TextField')()),
            ('snippets', self.gf('django.db.models.fields.TextField')()),
            ('triples', self.gf('django.db.models.fields.TextField')()),
            ('exact_answer', self.gf('django.db.models.fields.TextField')()),
            ('ideal_answer', self.gf('django.db.models.fields.TextField')()),
            ('testset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task1b.Detail1b'])),
        ))
        db.send_create_signal('task1b', ['golden_question_1b'])

        # Adding model 'user_results_1b'
        db.create_table('task1b_user_results_1b', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task1b.Detail1b'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('datatime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 28, 0, 0))),
        ))
        db.send_create_signal('task1b', ['user_results_1b'])

        # Adding model 'upload_information_for_1b'
        db.create_table('task1b_upload_information_for_1b', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task1b.Detail1b'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('task1b', ['upload_information_for_1b'])

        # Adding model 'evaluation_measures_1b'
        db.create_table('task1b_evaluation_measures_1b', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task1b.Detail1b'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('mp_con', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mr_con', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('f_con', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('MAP_con', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('GMAP_con', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mp_art', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mr_art', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('f_art', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('MAP_art', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('GMAP_art', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mp_snip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mr_snip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('f_snip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('MAP_snip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('GMAP_snip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mp_trip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mr_trip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('f_trip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('MAP_trip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('GMAP_trip', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('task1b', ['evaluation_measures_1b'])


    def backwards(self, orm):
        # Deleting model 'Detail1b'
        db.delete_table('task1b_detail1b')

        # Deleting model 'golden_question_1b'
        db.delete_table('task1b_golden_question_1b')

        # Deleting model 'user_results_1b'
        db.delete_table('task1b_user_results_1b')

        # Deleting model 'upload_information_for_1b'
        db.delete_table('task1b_upload_information_for_1b')

        # Deleting model 'evaluation_measures_1b'
        db.delete_table('task1b_evaluation_measures_1b')


    models = {
        'Test.system': {
            'Meta': {'object_name': 'system'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'system_description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'task1b.detail1b': {
            'Meta': {'object_name': 'Detail1b'},
            'downloaders': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.DateTimeField', [], {}),
            'golden_path': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_oracle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_downloads': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'number_of_questions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'started': ('django.db.models.fields.DateTimeField', [], {}),
            'test_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'task1b.evaluation_measures_1b': {
            'GMAP_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'GMAP_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'GMAP_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'GMAP_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'evaluation_measures_1b'},
            'f_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'f_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'f_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'f_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mp_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mp_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mp_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'testset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task1b.Detail1b']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"})
        },
        'task1b.golden_question_1b': {
            'Meta': {'object_name': 'golden_question_1b'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'concepts': ('django.db.models.fields.TextField', [], {}),
            'documents': ('django.db.models.fields.TextField', [], {}),
            'exact_answer': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ideal_answer': ('django.db.models.fields.TextField', [], {}),
            'question_id': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'snippets': ('django.db.models.fields.TextField', [], {}),
            'testset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task1b.Detail1b']"}),
            'triples': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        'task1b.upload_information_for_1b': {
            'Meta': {'object_name': 'upload_information_for_1b'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task1b.Detail1b']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'task1b.user_results_1b': {
            'Meta': {'object_name': 'user_results_1b'},
            'datatime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 28, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task1b.Detail1b']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['task1b']