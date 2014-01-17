# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Income.date_created'
        db.delete_column('customers_income', 'date_created')

        # Adding field 'Income.status'
        db.add_column('customers_income', 'status',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='opportunity'),
                      keep_default=False)

        # Adding field 'Income.date'
        db.add_column('customers_income', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True, default=datetime.datetime(2014, 1, 17, 0, 0)),
                      keep_default=False)

        # Deleting field 'Customer.status'
        db.delete_column('customers_customer', 'status')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Income.date_created'
        raise RuntimeError("Cannot reverse this migration. 'Income.date_created' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Income.date_created'
        db.add_column('customers_income', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True),
                      keep_default=False)

        # Deleting field 'Income.status'
        db.delete_column('customers_income', 'status')

        # Deleting field 'Income.date'
        db.delete_column('customers_income', 'date')

        # Adding field 'Customer.status'
        db.add_column('customers_customer', 'status',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default='opportunity'),
                      keep_default=False)


    models = {
        'accounts.company': {
            'Meta': {'object_name': 'Company'},
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postcode': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'street': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'})
        },
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Company']", 'related_name': "'users'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'unique': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_head': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trial': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
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
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
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
            'street': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'twitter': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '255'})
        },
        'customers.income': {
            'Meta': {'object_name': 'Income'},
            'amount': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '50'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']", 'related_name': "'incomes'"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True', 'default': 'datetime.datetime(2014, 1, 17, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'default': "'opportunity'"})
        }
    }

    complete_apps = ['customers']