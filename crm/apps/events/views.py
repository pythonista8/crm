import datetime as dt

from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from lib.date import LONG_MONTH_NAMES
from apps.events.forms import EventForm, MeetingForm, FollowUpForm
from apps.events.models import Event, FollowUp, Meeting


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
            messages.error(request, form.errors)
    else:
        form = EventForm()

    today = dt.date.today()
    if 'filter' in request.GET:
        date = dt.datetime.strptime(request.GET['filter'], '%d-%m-%Y').date()
    else:
        date = today

    from_ = dt.datetime(date.year, date.month, date.day)
    nextdate = date + dt.timedelta(days=1)
    to = dt.datetime(nextdate.year, nextdate.month, nextdate.day)

    followups = FollowUp.objects.filter(user__company=user.company, date=date)
    meetings = Meeting.objects.filter(
        Q(date_started__range=(from_, to)) | Q(date_ended__range=(from_, to)),
        user__company=user.company)

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

    ctx = {
        'event_form': form,
        'is_today': True if date == today else False,
        'followup_list': followups,
        'meeting_list': sorted(mdict.items()),
        'title': "My events",
        'title_icon': 'calendar-o',
        'date': '{month} {day}'.format(month=LONG_MONTH_NAMES[date.month-1],
                                       day=date.day)
    }
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


def toggle_status(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.is_done:
        event.is_done = False
        msg = "{event} is not done yet."
    else:
        event.is_done = True
        msg = "{event} is done!"
    event.save()
    title = event._meta.verbose_name.title()
    messages.success(request, msg.format(event=title))
    return redirect(reverse('events:index'))


def delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    title = event._meta.verbose_name.title()
    messages.success(
        request, "{event} has been deleted.".format(event=title))
    return redirect(reverse('events:index'))
