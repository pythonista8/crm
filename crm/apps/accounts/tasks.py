from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from celery import task


@task
def stop_trial(user):
    if user.is_trial and user.is_active:
        user.is_active = False
        user.save()


@task
def findout_experience(email):
    subject = "Greetings from Onekloud!"
    from_ = 'aldash@onekloud.com'

    html = mark_safe(
        render_to_string('accounts/customer_experience_email.html'))

    msg = EmailMessage(subject, html, from_, [email])
    msg.content_subtype = 'html'
    msg.send(fail_silently=False)
