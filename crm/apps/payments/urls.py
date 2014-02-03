from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.payments.views',
    url(r'^process/$', 'process', name='process'),
)
