from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.accounts.views',
    url(r'^signin/$', 'login_form', name="login"),
    url(r'^activate/$', 'activate_and_create_user', name="activate"),
)

urlpatterns += patterns(
    '',
    url(r'^signout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name="logout"),
)
