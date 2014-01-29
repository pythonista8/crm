import datetime as dt

from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from lib.date import LONG_MONTH_NAMES
from apps.events.forms import EventForm, MeetingForm, FollowUpForm
from apps.events.models import FollowUp, Meeting


def index(request):
    user = request.user
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(user=user)
            title = event._meta.verbose_name.title()
            messages.success(
                request, "{event} was added.".format(event=title))
    else:
        form = EventForm()

    ctx = dict(event_form=form)
    today = dt.date.today()
    from_ = dt.datetime(today.year, today.month, today.day)
    tmr = dt.date.today() + dt.timedelta(days=1)
    to = dt.datetime(tmr.year, tmr.month, tmr.day)

    followups = FollowUp.objects.filter(user__company=user.company, date=today)
    meetings = Meeting.objects.filter(
        user__company=user.company,
        Q(date_started__range=(from_, to)) | Q(date_ended__range=(from_, to)))

    if not user.is_head:
        followups = followups.filter(user=user)
        meetings = meetings.filter(user=user)

    mdict = dict()
    for m in meetings:
        # Keep data in `mdict` in a object-per-time format.
        # E.g. mdict[6] will retrieve a `Meeting` object at 6 o'clock.
        hr = str(m.date_started.hour)
        if len(hr) == 1:
            hr = '0' + hr
        min_ = str(m.date_started.minute)
        if len(min_) == 1:
            min_ = '0' + min_
        time = '{hr}:{min}'.format(hr=hr, min=min_)
        mdict[time] = m

    ctx['followup_list'] = followups
    ctx['meeting_list'] = sorted(mdict.items())

    meetings_title = Meeting._meta.verbose_name_plural.title()
    followups_title = FollowUp._meta.verbose_name_plural.title()
    ctx['title'] = "{meetings} & {followups}".format(
        meetings=meetings_title,
        followups=followups_title)

    ctx['title_icon'] = 'calendar-o'
    ctx['today'] = '{month} {day}'.format(
        month=LONG_MONTH_NAMES[today.month-1],
        day=today.day)
    return render(request, 'events/index.html', ctx)


class EventContextMixin(SuccessMessageMixin):
    model = None
    success_message = "Successfully updated"

    def get_context_data(self, **kwargs):
        ctx = super(EventContextMixin, self).get_context_data(**kwargs)
        ctx['title'] = "Edit {}".format(self.model._meta.verbose_name)
        ctx['title_icon'] = 'calendar-o'
        return ctx


class MeetingUpdate(EventContextMixin, UpdateView):
    model = Meeting
    form_class = MeetingForm

    def get_success_url(self):
        object_ = self.get_object()
        return reverse('events:edit-meeting', kwargs={'pk': object_.pk})


class FollowUpUpdate(EventContextMixin, UpdateView):
    model = FollowUp
    form_class = FollowUpForm

    def get_success_url(self):
        object_ = self.get_object()
        return reverse('events:edit-followup', kwargs={'pk': object_.pk})


def delete_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    meeting.delete()
    title = meeting._meta.verbose_name.title()
    messages.success(
        request, "{event} has been deleted.".format(event=title))
    return redirect(reverse('events:index'))


def delete_followup(request, pk):
    followup = get_object_or_404(FollowUp, pk=pk)
    followup.delete()
    title = followup._meta.verbose_name.title()
    messages.success(
        request, "{event} has been deleted.".format(event=title))
    return redirect(reverse('events:index'))
