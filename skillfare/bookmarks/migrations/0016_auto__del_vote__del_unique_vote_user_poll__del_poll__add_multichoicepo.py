# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['user', 'poll']
        db.delete_unique(u'bookmarks_vote', ['user_id', 'poll_id'])

        # Deleting model 'Vote'
        db.delete_table(u'bookmarks_vote')

        # Deleting model 'Poll'
        db.delete_table(u'bookmarks_poll')

        # Adding model 'MultiChoicePoll'
        db.create_table(u'bookmarks_multichoicepoll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'bookmarks', ['MultiChoicePoll'])

        # Adding model 'SingleChoiceVote'
        db.create_table(u'bookmarks_singlechoicevote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.SingleChoicePoll'])),
        ))
        db.send_create_signal(u'bookmarks', ['SingleChoiceVote'])

        # Adding unique constraint on 'SingleChoiceVote', fields ['user', 'poll']
        db.create_unique(u'bookmarks_singlechoicevote', ['user_id', 'poll_id'])

        # Adding model 'MultiChoiceVote'
        db.create_table(u'bookmarks_multichoicevote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.MultiChoicePoll'])),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Choice'])),
        ))
        db.send_create_signal(u'bookmarks', ['MultiChoiceVote'])

        # Adding unique constraint on 'MultiChoiceVote', fields ['user', 'poll']
        db.create_unique(u'bookmarks_multichoicevote', ['user_id', 'poll_id'])

        # Adding model 'SingleChoicePoll'
        db.create_table(u'bookmarks_singlechoicepoll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'bookmarks', ['SingleChoicePoll'])

        # Adding model 'SharedBookmark'
        db.create_table(u'bookmarks_sharedbookmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('bookmark', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bookmarks.Bookmark'], unique=True)),
            ('interest_poll', self.gf('django.db.models.fields.related.OneToOneField')(related_name='shared_bookmark', unique=True, to=orm['bookmarks.SingleChoicePoll'])),
            ('report_abuse_poll', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bookmarks.SingleChoicePoll'], unique=True)),
            ('hot_score', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'bookmarks', ['SharedBookmark'])


        # Changing field 'Choice.poll'
        db.alter_column(u'bookmarks_choice', 'poll_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.MultiChoicePoll']))

        # Changing field 'Link.learn_level_poll'
        db.alter_column(u'bookmarks_link', 'learn_level_poll_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bookmarks.MultiChoicePoll'], unique=True))

    def backwards(self, orm):
        # Removing unique constraint on 'MultiChoiceVote', fields ['user', 'poll']
        db.delete_unique(u'bookmarks_multichoicevote', ['user_id', 'poll_id'])

        # Removing unique constraint on 'SingleChoiceVote', fields ['user', 'poll']
        db.delete_unique(u'bookmarks_singlechoicevote', ['user_id', 'poll_id'])

        # Adding model 'Vote'
        db.create_table(u'bookmarks_vote', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Poll'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Choice'])),
        ))
        db.send_create_signal(u'bookmarks', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'poll']
        db.create_unique(u'bookmarks_vote', ['user_id', 'poll_id'])

        # Adding model 'Poll'
        db.create_table(u'bookmarks_poll', (
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'bookmarks', ['Poll'])

        # Deleting model 'MultiChoicePoll'
        db.delete_table(u'bookmarks_multichoicepoll')

        # Deleting model 'SingleChoiceVote'
        db.delete_table(u'bookmarks_singlechoicevote')

        # Deleting model 'MultiChoiceVote'
        db.delete_table(u'bookmarks_multichoicevote')

        # Deleting model 'SingleChoicePoll'
        db.delete_table(u'bookmarks_singlechoicepoll')

        # Deleting model 'SharedBookmark'
        db.delete_table(u'bookmarks_sharedbookmark')


        # Changing field 'Choice.poll'
        db.alter_column(u'bookmarks_choice', 'poll_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Poll']))

        # Changing field 'Link.learn_level_poll'
        db.alter_column(u'bookmarks_link', 'learn_level_poll_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bookmarks.Poll'], unique=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bookmarks.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bookmarks.Feature']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.Link']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bookmarks.choice': {
            'Meta': {'ordering': "['pos']", 'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.MultiChoicePoll']"}),
            'pos': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'bookmarks.feature': {
            'Meta': {'ordering': "['description']", 'object_name': 'Feature'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'bookmarks.link': {
            'Meta': {'object_name': 'Link'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learn_level_poll': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bookmarks.MultiChoicePoll']", 'unique': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'bookmarks.multichoicepoll': {
            'Meta': {'object_name': 'MultiChoicePoll'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bookmarks.multichoicevote': {
            'Meta': {'unique_together': "(('user', 'poll'),)", 'object_name': 'MultiChoiceVote'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.Choice']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.MultiChoicePoll']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bookmarks.sharedbookmark': {
            'Meta': {'object_name': 'SharedBookmark'},
            'bookmark': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bookmarks.Bookmark']", 'unique': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'hot_score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_poll': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'shared_bookmark'", 'unique': 'True', 'to': u"orm['bookmarks.SingleChoicePoll']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'report_abuse_poll': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bookmarks.SingleChoicePoll']", 'unique': 'True'})
        },
        u'bookmarks.singlechoicepoll': {
            'Meta': {'object_name': 'SingleChoicePoll'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bookmarks.singlechoicevote': {
            'Meta': {'unique_together': "(('user', 'poll'),)", 'object_name': 'SingleChoiceVote'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.SingleChoicePoll']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['bookmarks']