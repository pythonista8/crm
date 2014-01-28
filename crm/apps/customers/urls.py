from django.conf.urls import patterns, url
from apps.customers import views


urlpatterns = patterns(
    '',
    url(r'^$', views.CustomerList.as_view(), name="list"),
    url(r'^new/$', views.CustomerCreate.as_view(), name="create"),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_customer,
        name="delete-customer"),
    url(r'^(?P<pk>\d+)/$', views.CustomerUpdate.as_view(), name="edit"),
    url(r'^(?P<pk>\d+)/amounts/$', views.AmountList.as_view(),
        name="amount-list"),
)
