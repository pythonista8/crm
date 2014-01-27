import time
import datetime as dt

from django import forms
from django.core.exceptions import ValidationError
from lib.date import parsedate
from apps.events.models import Meeting, FollowUp


class EventForm(forms.Form):
    text = forms.CharField()
    hours = forms.IntegerField(
        min_value=0, max_value=24, initial=1, required=False)
    minutes = forms.IntegerField(
        min_value=0, max_value=60, initial=0, required=False)

    def clean_text(self):
        text = self.cleaned_data['text']
        try:
            parsedate(text)
        except ValueError:
            msg = "Could not obtain date. Please add."
            raise ValidationError("%(value)s", code='invalid',
                                  params=dict(value=msg))
        return text

    def save(self, user):
        text = self.cleaned_data['text']
        datedict = parsedate(text)
        f = '%m %d %Y'
        dates = "{mon} {day} {yr}".format(mon=datedict['month'],
                                          day=datedict['day'],
                                          yr=datedict['year'])
        if 'hours' in datedict:  # Meeting
            startdate = dates + " {hr}:{min}".format(hr=datedict['hours'],
                                                     min=datedict['minutes'])
            f += ' %H:%M'
            starttime = time.mktime(time.strptime(startdate, f))
            date_started = dt.datetime.fromtimestamp(starttime)
            hr = self.cleaned_data['hours']
            min_ = self.cleaned_data['minutes']
            enddate = dates + " {hr}:{min}".format(
                hr=hr + int(datedict['hours']),
                min=min_ + int(datedict['minutes']))
            endtime = time.mktime(time.strptime(enddate, f))
            date_ended = dt.datetime.fromtimestamp(endtime)
            event = Meeting.objects.create(date_started=date_started,
                                           date_ended=date_ended,
                                           user=user)
        else:  # Follow-Up
            date = dt.datetime.strptime(dates, f).date()
            event = FollowUp.objects.create(date=date, user=user)
        event.subject = self.cleaned_data['text']
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
