from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from lib.encrypt import hmac_sha256
from apps.accounts.forms import LoginForm
from apps.accounts.models import User, Company


def login_form(request):
    success_url = reverse('events:index')
    if request.user.is_authenticated():
        return redirect(success_url)
    email = None
    if request.method == 'POST':
        email = request.POST['email']
        passw = request.POST['password']
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


def create_user(request):
    if request.method == 'POST':
        reqhash = request.META['Authorization']
        hash_ = hmac_sha256(
            '{email}{key}{company}'.format(key=settings.HMAC_KEY,
                                           email=request.POST['email'],
                                           company=request.POST['company']))
        if reqhash != hash_:
            return http.HttpResponse(status_code=400)

        email = request.POST['email']
        password = request.POST['password']
        cname = request.POST['company']

        company = Company.objects.create(name=cname)
        user = User.objects.create_user(email, password, company=company)
        return http.HttpResponse(user.email)

    return http.HttpResponseNotAllowed(['GET'])
