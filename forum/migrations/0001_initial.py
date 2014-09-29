# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('forum_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Category'])

        # Adding model 'Forum'
        db.create_table('forum_forum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forums', to=orm['forum.Category'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True, blank=True)),
            ('topic_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('post_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('forum', ['Forum'])

        # Adding model 'Topic'
        db.create_table('forum_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topics', to=orm['forum.Forum'])),
            ('post_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('forum', ['Topic'])

        # Adding model 'Post'
        db.create_table('forum_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['forum.Topic'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('forum', ['Post'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('forum_category')

        # Deleting model 'Forum'
        db.delete_table('forum_forum')

        # Deleting model 'Topic'
        db.delete_table('forum_topic')

        # Deleting model 'Post'
        db.delete_table('forum_post')


    models = {
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
        'forum.category': {
            'Meta': {'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'})
        },
        'forum.forum': {
            'Meta': {'object_name': 'Forum'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forums'", 'to': "orm['forum.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'topic_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'forum.post': {
            'Meta': {'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['forum.Topic']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'forum.topic': {
            'Meta': {'object_name': 'Topic'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['forum']