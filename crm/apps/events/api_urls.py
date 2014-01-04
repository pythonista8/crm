from django.conf.urls import patterns, url
from apps.events import api

urlpatterns = patterns(
    '',
    url(r'^eventDetails/$', api.event_details, name='event_details'),
)
