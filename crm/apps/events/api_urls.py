from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.events.api',
    url(r'^eventsDates/$',
        'dates',
        name='dates'),

    url(r'^eventDetails/$',
        'details',
        name='details'),

    url(r'^filterByDate/$',
        'filter_by_date',
        name='filter_by_date'),
)
