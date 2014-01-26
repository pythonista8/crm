from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from celery import task
from apps.accounts.models import User


@task
def stop_trial(user_pk):
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return None
    else:
        if user.is_trial and user.is_active:
            user.is_active = False
            user.save()


@task
def test_stop_trial(user_pk):
    try:
        user = User.objects.get(email='aldash@onekloud.com')
    except User.DoesNotExist:
        return None
    else:
        if user.is_trial and user.is_active:
            user.is_active = False
            user.save()


@task
def findout_experience(email):
    subject = "Greetings from Onekloud!"
    from_ = 'samantha@onekloud.com'

    html = mark_safe(
        render_to_string('accounts/customer_experience_email.html'))

    msg = EmailMessage(subject, html, from_, [email])
    msg.content_subtype = 'html'
    msg.send(fail_silently=True)
