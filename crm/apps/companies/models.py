"""Company models.

These classes are describing a Company.
"""
import datetime as dt

from django.db import models
from django.core.urlresolvers import reverse


class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    postcode = models.PositiveIntegerField(blank=True, null=True)

    # Date Records.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.date_modified = dt.datetime.now()
        super(Company, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('companies:edit', kwargs={'pk': self.pk})
