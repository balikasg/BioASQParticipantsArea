# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'eval_meas_oracle_1b'
        db.create_table('oracle_eval_meas_oracle_1b', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task1b.Detail1b'])),
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
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 8, 0, 0))),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('oracle', ['eval_meas_oracle_1b'])


    def backwards(self, orm):
        # Deleting model 'eval_meas_oracle_1b'
        db.delete_table('oracle_eval_meas_oracle_1b')


    models = {
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
        'oracle.eval_meas_oracle': {
            'Meta': {'object_name': 'eval_meas_oracle'},
            'accuracy': ('django.db.models.fields.FloatField', [], {}),
            'ebp': ('django.db.models.fields.FloatField', [], {}),
            'example_based_f': ('django.db.models.fields.FloatField', [], {}),
            'example_based_recall': ('django.db.models.fields.FloatField', [], {}),
            'hierarchical_f': ('django.db.models.fields.FloatField', [], {}),
            'hierarchical_precision': ('django.db.models.fields.FloatField', [], {}),
            'hierarchical_recall': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 8, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"})
        },
        'oracle.eval_meas_oracle_1b': {
            'GMAP_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'GMAP_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'GMAP_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'GMAP_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MAP_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'eval_meas_oracle_1b'},
            'f_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'f_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'f_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'f_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mp_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mp_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mp_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mp_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_art': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_con': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_snip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mr_trip': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['task1b.Detail1b']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 8, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"})
        },
        'oracle.log_oracle': {
            'Meta': {'object_name': 'log_oracle'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1900', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.system']"}),
            'test_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Test.Detail']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        }
    }

    complete_apps = ['oracle']