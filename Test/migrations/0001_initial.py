# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Detail'
        db.create_table('Test_detail', (
            ('test_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('started', self.gf('django.db.models.fields.DateTimeField')()),
            ('finished', self.gf('django.db.models.fields.DateTimeField')()),
            ('number_of_abstracts', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number_of_abstracts_annotated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number_of_downloads', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('number_of_abstracts_oracle', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('path_raw', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('path_vect', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('downloaders', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_oracle', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Test', ['Detail'])

        # Adding model 'Article'
        db.create_table('Test_article', (
            ('distro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Detail'])),
            ('pmid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('abstract', self.gf('django.db.models.fields.CharField')(max_length=10000, null=True, blank=True)),
        ))
        db.send_create_signal('Test', ['Article'])

        # Adding model 'bioasq_baseline'
        db.create_table('Test_bioasq_baseline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('distro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Detail'])),
            ('pmid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Article'])),
            ('mesh', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal('Test', ['bioasq_baseline'])

        # Adding model 'user_profile'
        db.create_table('Test_user_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('task1a', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('task1b1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('task1b2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('task2a', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('task2b', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('receive_information', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Test', ['user_profile'])

        # Adding model 'system'
        db.create_table('Test_system', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('system', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('system_description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('Test', ['system'])

        # Adding model 'test_result'
        db.create_table('Test_test_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Detail'])),
            ('pmid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Article'])),
            ('mesh', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal('Test', ['test_result'])

        # Adding model 'test_result_file'
        db.create_table('Test_test_result_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Detail'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('Test', ['test_result_file'])

        # Adding model 'upload_information'
        db.create_table('Test_upload_information', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Detail'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('Test', ['upload_information'])

        # Adding model 'eval_meas'
        db.create_table('Test_eval_meas', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.Detail'])),
            ('accuracy', self.gf('django.db.models.fields.FloatField')()),
            ('ebp', self.gf('django.db.models.fields.FloatField')()),
            ('example_based_recall', self.gf('django.db.models.fields.FloatField')()),
            ('example_based_f', self.gf('django.db.models.fields.FloatField')()),
            ('macro_precision', self.gf('django.db.models.fields.FloatField')()),
            ('macro_recall', self.gf('django.db.models.fields.FloatField')()),
            ('macro_f_measure', self.gf('django.db.models.fields.FloatField')()),
            ('micro_precision', self.gf('django.db.models.fields.FloatField')()),
            ('micro_recall', self.gf('django.db.models.fields.FloatField')()),
            ('micro_f', self.gf('django.db.models.fields.FloatField')()),
            ('hierarchical_precision', self.gf('django.db.models.fields.FloatField')()),
            ('hierarchical_recall', self.gf('django.db.models.fields.FloatField')()),
            ('hierarchical_f', self.gf('django.db.models.fields.FloatField')()),
            ('lca_p', self.gf('django.db.models.fields.FloatField')()),
            ('lca_r', self.gf('django.db.models.fields.FloatField')()),
            ('lca_f', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('Test', ['eval_meas'])


    def backwards(self, orm):
        # Deleting model 'Detail'
        db.delete_table('Test_detail')

        # Deleting model 'Article'
        db.delete_table('Test_article')

        # Deleting model 'bioasq_baseline'
        db.delete_table('Test_bioasq_baseline')

        # Deleting model 'user_profile'
        db.delete_table('Test_user_profile')

        # Deleting model 'system'
        db.delete_table('Test_system')

        # Deleting model 'test_result'
        db.delete_table('Test_test_result')

        # Deleting model 'test_result_file'
        db.delete_table('Test_test_result_file')

        # Deleting model 'upload_information'
        db.delete_table('Test_upload_information')

        # Deleting model 'eval_meas'
        db.delete_table('Test_eval_meas')


    models = {
        'Test.article': {
            'Meta': {'ordering': "['-pmid']", 'object_name': 'Article'},
            'abstract': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'distro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Detail']"}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'Test.bioasq_baseline': {
            'Meta': {'object_name': 'bioasq_baseline'},
            'distro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Detail']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mesh': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'pmid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Article']"})
        },
        'Test.detail': {
            'Meta': {'object_name': 'Detail'},
            'downloaders': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.DateTimeField', [], {}),
            'is_oracle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_abstracts': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_abstracts_annotated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_abstracts_oracle': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'number_of_downloads': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'path_raw': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'path_vect': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {}),
            'test_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'Test.eval_meas': {
            'Meta': {'object_name': 'eval_meas'},
            'accuracy': ('django.db.models.fields.FloatField', [], {}),
            'ebp': ('django.db.models.fields.FloatField', [], {}),
            'example_based_f': ('django.db.models.fields.FloatField', [], {}),
            'example_based_recall': ('django.db.models.fields.FloatField', [], {}),
            'hierarchical_f': ('django.db.models.fields.FloatField', [], {}),
            'hierarchical_precision': ('django.db.models.fields.FloatField', [], {}),
            'hierarchical_recall': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lca_f': ('django.db.models.fields.FloatField', [], {}),
            'lca_p': ('django.db.models.fields.FloatField', [], {}),
            'lca_r': ('django.db.models.fields.FloatField', [], {}),
            'macro_f_measure': ('django.db.models.fields.FloatField', [], {}),
            'macro_precision': ('django.db.models.fields.FloatField', [], {}),
            'macro_recall': ('django.db.models.fields.FloatField', [], {}),
            'micro_f': ('django.db.models.fields.FloatField', [], {}),
            'micro_precision': ('django.db.models.fields.FloatField', [], {}),
            'micro_recall': ('django.db.models.fields.FloatField', [], {}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Detail']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"})
        },
        'Test.system': {
            'Meta': {'object_name': 'system'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'system_description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Test.test_result': {
            'Meta': {'object_name': 'test_result'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mesh': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'pmid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Article']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Detail']"})
        },
        'Test.test_result_file': {
            'Meta': {'object_name': 'test_result_file'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Detail']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Test.upload_information': {
            'Meta': {'object_name': 'upload_information'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Detail']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Test.user_profile': {
            'Meta': {'object_name': 'user_profile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'receive_information': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task1a': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task1b1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task1b2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task2a': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'task2b': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
        }
    }

    complete_apps = ['Test']