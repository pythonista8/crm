from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.events.api.views',

    url(r'^eventsDates/$',
        'dates',
        name='dates'),
)
