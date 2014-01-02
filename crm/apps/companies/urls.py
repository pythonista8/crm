from django.conf.urls import patterns, url
from apps.companies import views


urlpatterns = patterns(
    '',
    url(r'^$', views.CompanyList.as_view(), name="list"),
    url(r'^new/$', views.CompanyCreate.as_view(), name="create"),
    url(r'^(?P<pk>\d+)/$', views.CompanyUpdate.as_view(), name="edit"),
)
