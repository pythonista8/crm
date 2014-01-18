from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class PermissionMiddleware(object):
    def process_request(self, request):
        exc_urls = [reverse('accounts:activate-trial')]
        granted = False
        for url in exc_urls:
            if url in request.path:
                granted = True

        login_url = reverse('accounts:login')
        on_login_page = login_url in request.path
        logged_in = request.user.is_authenticated()

        if not granted and not logged_in and not on_login_page:
            return redirect(login_url)


class RedirectMiddleware(object):
    def process_request(self, request):
        if request.path == '/':
            return redirect(reverse('events:index'))
