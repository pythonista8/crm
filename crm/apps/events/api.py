import json

from django import http
from lib.date import parsedate


def event_details(request):
    if request.method == 'GET':
        s = request.GET['s']
        try:
            datedict = parsedate(s, month_as_str=True)
        except ValueError:
            res = dict()
        else:
            res = dict(status='success', data=datedict)
        return http.HttpResponse(
            json.dumps(res), content_type='application/json')
    return http.HttpResponseNotAllowed(['POST'])
