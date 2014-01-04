from django.conf.urls import patterns, include, url
from apps.events import views

urlpatterns = patterns(
    'apps.events.views',
    url(r'^$', 'index', name='index'),
    url(r'^delete-meeting/(?P<pk>\d+)/$', 'delete_meeting',
        name='delete-meeting'),
    url(r'^delete-followup/(?P<pk>\d+)/$', 'delete_followup',
        name='delete-followup'),
)

urlpatterns += patterns(
    '',
    url(r'^api/', include('apps.events.api_urls', namespace='api')),
    url(r'^meetings/(?P<pk>\d+)/$', views.MeetingUpdate.as_view(),
        name='edit-meeting'),
    url(r'^followups/(?P<pk>\d+)/$', views.FollowUpUpdate.as_view(),
        name='edit-followup'),
)
