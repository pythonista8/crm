from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.reports.views',
    url(r'^$', 'index', name='index'),
    url(r'^export-customers/$', 'export_customers', name='export-customers'),
    url(r'^export-amounts/$', 'export_amounts', name='export-amounts'),
)
