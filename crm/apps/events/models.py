import datetime as dt

from django.db import models
from django.core.urlresolvers import reverse
from apps.accounts.models import User


class Event(models.Model):
    subject = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.date_modified = dt.datetime.now()
        super(Event, self).save(*args, **kwargs)


class FollowUp(Event):
    user = models.ForeignKey(User, related_name='followups')
    date = models.DateField()

    class Meta:
        verbose_name = "follow-up"
        verbose_name_plural = "follow-ups"

    def get_absolute_url(self):
        return reverse('events:edit-followup', args=[self.pk])


class Meeting(Event):
    user = models.ForeignKey(User, related_name='meetings')

    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()

    class Meta:
        verbose_name = "meeting"
        verbose_name_plural = "meetings"

    def get_absolute_url(self):
        return reverse('events:edit-meeting', args=[self.pk])
