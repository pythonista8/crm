import hashlib

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from apps.accounts.forms import LoginForm
from apps.accounts.models import User, Company


def login_form(request):
    success_url = reverse('events:index')
    if request.user.is_authenticated():
        return redirect(success_url)

    email = None
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')
        user = authenticate(email=email, password=passw)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(
                    request, "Welcome, {name}!".format(
                        name=user.get_short_name()))
                return redirect(success_url)
            else:
                messages.error(request, "Your account is disabled. Contact to "
                                        "administrator")
        else:
            messages.error(request, "Your email or password is incorrect.")

    if email is not None:
        form = LoginForm(initial=dict(email=email))
    else:
        form = LoginForm()

    return render(request, 'accounts/login_form.html', dict(form=form))


def activate_trial(request):
    if request.method == 'GET':
        reqhash = request.GET.get('key')
        email = request.GET.get('email')
        cname = request.GET.get('company')

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            key = '{key}{email}{company}'.format(
                key=settings.ACTIVATION_SALT, email=email, company=cname
            ).encode('utf8')

            hash_ = hashlib.md5(key).hexdigest()
            if reqhash != hash_:
                return http.HttpResponseForbidden()

            passw = 'demo'
            company = Company.objects.create(name=cname)
            User.objects.create_user(email, passw, company=company)
            user = authenticate(email=email, password=passw)
            login(request, user)
            messages.success(request, "Welcome, {name}!".format(
                name=user.get_short_name()))

            # Notify admins about new user.
            subject = "New user at Onekloud CRM!"
            support_email = 'support@onekloud.com'
            recipients = ('aldash@onekloud.com', 'samantha@onekloud.com')
            data = dict(email=user.email, company=user.company)
            html = mark_safe(
                render_to_string('accounts/notification_email.html', data))
            msg = EmailMessage(subject, html, support_email, recipients)
            msg.content_subtype = 'html'
            msg.send(fail_silently=True)
            return redirect(reverse('events:index'))
        else:
            return redirect(reverse('accounts:login'))

    return http.HttpResponseNotAllowed(['POST'])
