from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class PermissionMiddleware(object):
    def process_request(self, request):
        login_url = reverse('accounts:login')
        on_login_page = login_url in request.path
        logged_in = request.user.is_authenticated()
        if not logged_in and not on_login_page:
            return redirect(login_url)
