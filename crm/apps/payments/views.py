from django import http
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process(request):
    if request.method == 'POST':
        ref = request.META.get('HTTP_REFERER', None)
        if 'www.2checkout.com' in ref:
            return http.HttpResponse(str(request.POST))
        else:
            return http.HttpResponseForbidden()
    else:
        return http.HttpResponseNotAllowed('GET')
