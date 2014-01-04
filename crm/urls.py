from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('apps.events.urls', namespace='events')),
    url(r'^auth/', include('apps.accounts.urls', namespace='accounts')),
    url(r'^customers/', include('apps.customers.urls', namespace='customers')),
    url(r'^companies/', include('apps.companies.urls', namespace='companies')),
    url(r'^reports/', include('apps.reports.urls', namespace='reports')),
    url(r'^admin/', include(admin.site.urls)),
)
