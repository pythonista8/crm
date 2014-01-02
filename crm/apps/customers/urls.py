from django.conf.urls import patterns, url
from apps.customers import views


urlpatterns = patterns(
    '',
    url(r'^$', views.CustomerList.as_view(), name="list"),
    url(r'^new/$', views.CustomerCreate.as_view(), name="create"),
    url(r'^(?P<pk>\d+)/$', views.CustomerUpdate.as_view(), name="edit"),
)
