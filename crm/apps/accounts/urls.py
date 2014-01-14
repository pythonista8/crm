from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.accounts.views',
    url(r'^signin/$', 'login_form', name="login"),
    url(r'^create_user/$', 'create_user', name="create_user"),
)

urlpatterns += patterns(
    '',
    url(r'^signout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name="logout"),
)
