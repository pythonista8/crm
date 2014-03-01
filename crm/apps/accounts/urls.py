from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.accounts.views',

    url(r'^signin/$',
        'login_form',
        name="login"),

    url(r'^try/$',
        'activate_trial',
        name="activate_trial"),

    url(r'^subscribe/$',
        'activate_subscription',
        name="activate_subscription"),
)

urlpatterns += patterns(
    '',

    url(r'^signout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name="logout"),
)
