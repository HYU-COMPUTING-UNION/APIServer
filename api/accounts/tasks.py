from __future__ import absolute_import
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_confirmation_mail(subject, message, from_email, recipients):
    send_mail(subject, message, from_email, recipients)
