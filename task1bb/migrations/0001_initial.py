# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'user_results_1bb'
        db.create_table('task1bb_user_results_1bb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task1b.Detail1b'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 28, 0, 0))),
        ))
        db.send_create_signal('task1bb', ['user_results_1bb'])

        # Adding model 'evaluation_measures_1bb'
        db.create_table('task1bb_evaluation_measures_1bb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task1b.Detail1b'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Test.system'])),
            ('acc', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('s_acc', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('l_acc', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mrr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prec', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rec', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('fmeas', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('r2p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('r2r', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('r2f', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('r4p', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('r4r', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('r4f', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('read', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('recall', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rep', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('preci', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('task1bb', ['evaluation_measures_1bb'])


    def backwards(self, orm):
        # Deleting model 'user_results_1bb'
        db.delete_table('task1bb_user_results_1bb')

        # Deleting model 'evaluation_measures_1bb'
        db.delete_table('task1bb_evaluation_measures_1bb')


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
        'task1bb.evaluation_measures_1bb': {
            'Meta': {'object_name': 'evaluation_measures_1bb'},
            'acc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fmeas': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_acc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mrr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prec': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'preci': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'r2f': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'r2p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'r2r': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'r4f': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'r4p': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'r4r': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'read': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rec': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'recall': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rep': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            's_acc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'testset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task1b.Detail1b']"})
        },
        'task1bb.user_results_1bb': {
            'Meta': {'object_name': 'user_results_1bb'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 28, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task1b.Detail1b']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['task1bb']