import datetime as dt

from django.db import models
from apps.accounts.models import User


class Event(models.Model):
    subject = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.date_modified = dt.datetime.now()
        super(Event, self).save(*args, **kwargs)


class FollowUp(Event):
    date = models.DateField()

    class Meta:
        verbose_name = "follow-up"
        verbose_name_plural = "follow-ups"


class Meeting(Event):
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()

    class Meta:
        verbose_name = "meeting"
        verbose_name_plural = "meetings"
