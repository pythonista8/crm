import time
import datetime as dt

from django import forms
from django.core.exceptions import ValidationError
from lib.date import parsedate
from apps.events.models import Meeting, FollowUp


class EventForm(forms.Form):
    task = forms.CharField()

    def clean_task(self):
        data = self.cleaned_data['task']
        try:
            parsedate(data)
        except ValueError:
            raise ValidationError("Please add a date.")
        return data

    def save(self, user):
        task = self.cleaned_data['task']
        datedict = parsedate(task)
        f = '%m %d %Y'
        is_meeting = 'hours' in datedict
        dates = "{mon} {day} {yr}".format(mon=datedict['month'],
                                          day=datedict['day'],
                                          yr=datedict['year'])
        if is_meeting:
            startdate = dates + " {hr}:{min}".format(hr=datedict['hours'],
                                                     min=datedict['minutes'])
            f += ' %H:%M'
            starttime = time.mktime(time.strptime(startdate, f))
            date_started = dt.datetime.fromtimestamp(starttime)

            date_ended = date_started + dt.timedelta(hours=1)
            event = Meeting.objects.create(date_started=date_started,
                                           date_ended=date_ended,
                                           user=user)
        else:  # Follow-Up
            date = dt.datetime.strptime(dates, f).date()
            event = FollowUp.objects.create(date=date, user=user)
        event.subject = task
        event.save()
        return event


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ('user', 'date_created', 'date_modified')


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        exclude = ('user', 'date_created', 'date_modified')
