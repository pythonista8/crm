from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^', include('apps.events.urls', namespace='events')),
    url(r'^auth/', include('apps.accounts.urls', namespace='accounts')),
    url(r'^customers/', include('apps.customers.urls', namespace='customers')),
    url(r'^reports/', include('apps.reports.urls', namespace='reports')),
)
