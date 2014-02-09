import json
import datetime as dt

from django import http
from apps.events.models import FollowUp, Meeting


def dates(request):
    if request.method == 'GET':
        user = request.user
        meeting_qs = Meeting.objects.filter(user__company=user.company)
        followup_qs = FollowUp.objects.filter(user__company=user.company)
        if not user.is_head:
            meeting_qs = meeting_qs.filter(user=user)
            followup_qs = followup_qs.filter(user=user)
        f = '%d-%m-%Y'
        datelist = list()
        for ob in meeting_qs:
            date = dt.datetime.strftime(ob.date_started, f)
            if not date in datelist:
                datelist.append(date)
        for ob in followup_qs:
            date = dt.datetime.strftime(ob.date, f)
            if not date in datelist:
                datelist.append(date)
        res = dict(status='success', data=datelist)
        return http.HttpResponse(
            json.dumps(res), content_type='application/json')
    return http.HttpResponseNotAllowed(['POST'])
