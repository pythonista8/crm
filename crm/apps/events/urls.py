from django.conf.urls import patterns, url
from apps.events import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^meetings/(?P<pk>\d+)/$', views.MeetingUpdate.as_view(),
        name='edit-meeting'),
    url(r'^followups/(?P<pk>\d+)/$', views.FollowUpUpdate.as_view(),
        name='edit-followup'),
)
