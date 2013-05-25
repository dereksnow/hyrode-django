# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MultiChoiceVote', fields ['user', 'poll']
        db.delete_unique(u'bookmarks_multichoicevote', ['user_id', 'poll_id'])

        # Removing unique constraint on 'SingleChoiceVote', fields ['user', 'poll']
        db.delete_unique(u'bookmarks_singlechoicevote', ['user_id', 'poll_id'])

        # Deleting model 'SingleChoiceVote'
        db.delete_table(u'bookmarks_singlechoicevote')

        # Deleting model 'MultiChoiceVote'
        db.delete_table(u'bookmarks_multichoicevote')

        # Adding model 'AbuseVote'
        db.create_table(u'bookmarks_abusevote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('shared_bookmark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.SharedBookmark'])),
        ))
        db.send_create_signal(u'bookmarks', ['AbuseVote'])

        # Adding model 'LevelVote'
        db.create_table(u'bookmarks_levelvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('learn_level', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Link'])),
        ))
        db.send_create_signal(u'bookmarks', ['LevelVote'])

        # Adding model 'LikeVote'
        db.create_table(u'bookmarks_likevote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('shared_bookmark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.SharedBookmark'])),
        ))
        db.send_create_signal(u'bookmarks', ['LikeVote'])

        # Deleting field 'Link.learn_level_poll'
        db.delete_column(u'bookmarks_link', 'learn_level_poll_id')

        # Deleting field 'SharedBookmark.report_abuse_poll'
        db.delete_column(u'bookmarks_sharedbookmark', 'report_abuse_poll_id')

        # Deleting field 'SharedBookmark.interest_poll'
        db.delete_column(u'bookmarks_sharedbookmark', 'interest_poll_id')


    def backwards(self, orm):
        # Adding model 'SingleChoiceVote'
        db.create_table(u'bookmarks_singlechoicevote', (
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.SingleChoicePoll'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'bookmarks', ['SingleChoiceVote'])

        # Adding unique constraint on 'SingleChoiceVote', fields ['user', 'poll']
        db.create_unique(u'bookmarks_singlechoicevote', ['user_id', 'poll_id'])

        # Adding model 'MultiChoiceVote'
        db.create_table(u'bookmarks_multichoicevote', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.MultiChoicePoll'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Choice'])),
        ))
        db.send_create_signal(u'bookmarks', ['MultiChoiceVote'])

        # Adding unique constraint on 'MultiChoiceVote', fields ['user', 'poll']
        db.create_unique(u'bookmarks_multichoicevote', ['user_id', 'poll_id'])

        # Deleting model 'AbuseVote'
        db.delete_table(u'bookmarks_abusevote')

        # Deleting model 'LevelVote'
        db.delete_table(u'bookmarks_levelvote')

        # Deleting model 'LikeVote'
        db.delete_table(u'bookmarks_likevote')

        # Adding field 'Link.learn_level_poll'
        db.add_column(u'bookmarks_link', 'learn_level_poll',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['bookmarks.MultiChoicePoll'], unique=True),
                      keep_default=False)

        # Adding field 'SharedBookmark.report_abuse_poll'
        db.add_column(u'bookmarks_sharedbookmark', 'report_abuse_poll',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['bookmarks.SingleChoicePoll'], unique=True),
                      keep_default=False)

        # Adding field 'SharedBookmark.interest_poll'
        db.add_column(u'bookmarks_sharedbookmark', 'interest_poll',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, related_name='shared_bookmark', unique=True, to=orm['bookmarks.SingleChoicePoll']),
                      keep_default=False)


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
        u'bookmarks.abusevote': {
            'Meta': {'object_name': 'AbuseVote'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shared_bookmark': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.SharedBookmark']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bookmarks.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bookmarks.Feature']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.Link']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'personal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        u'bookmarks.levelvote': {
            'Meta': {'object_name': 'LevelVote'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'learn_level': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.Link']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bookmarks.likevote': {
            'Meta': {'object_name': 'LikeVote'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'shared_bookmark': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.SharedBookmark']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bookmarks.link': {
            'Meta': {'object_name': 'Link'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        u'bookmarks.sharedbookmark': {
            'Meta': {'object_name': 'SharedBookmark'},
            'bookmark': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bookmarks.Bookmark']", 'unique': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'hot_score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'bookmarks.singlechoicepoll': {
            'Meta': {'object_name': 'SingleChoicePoll'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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