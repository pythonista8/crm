from django.conf.urls import patterns, url
from apps.accounts import views


urlpatterns = patterns(
    '',
    url(r'^signin/$', views.login_form, name="login"),
    url(r'^signout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name="signout"),
)
