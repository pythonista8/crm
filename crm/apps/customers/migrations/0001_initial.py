# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table('customers_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255, default='opportunity')),
            ('amount', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, blank=True, max_digits=50, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('salutation', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('position', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('company', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('website', self.gf('django.db.models.fields.URLField')(blank=True, max_length=255)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(blank=True, max_length=255)),
            ('googleplus', self.gf('django.db.models.fields.URLField')(blank=True, max_length=255)),
            ('twitter', self.gf('django.db.models.fields.URLField')(blank=True, max_length=255)),
            ('linkedin', self.gf('django.db.models.fields.URLField')(blank=True, max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('skype', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('cell_phone', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('main_phone', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('street', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('postcode', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('customers', ['Customer'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table('customers_customer')


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'amount': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'blank': 'True', 'max_digits': '50', 'null': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'company': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'facebook': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'googleplus': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'linkedin': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'main_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'postcode': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'salutation': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'skype': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'opportunity'"}),
            'street': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'twitter': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['customers']