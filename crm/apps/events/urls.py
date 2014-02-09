from django.conf.urls import patterns, include, url
from apps.events import views

urlpatterns = patterns(
    'apps.events.views',

    url(r'^$',
        'index',
        name='index'),

    url(r'^toggle-status/(?P<pk>\d+)/$',
        'toggle_status',
        name='toggle-status'),

    url(r'^delete/(?P<pk>\d+)/$',
        'delete',
        name='delete'),
)

urlpatterns += patterns(
    '',

    url(r'^api/',
        include('apps.events.api.urls', namespace='api')),

    url(r'^meetings/(?P<pk>\d+)/$',
        views.MeetingUpdate.as_view(),
        name='edit-meeting'),

    url(r'^followups/(?P<pk>\d+)/$',
        views.FollowUpUpdate.as_view(),
        name='edit-followup'),
)
