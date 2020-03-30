from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings
from django.urls import reverse


@shared_task
def send_emial_aync(subject, message, email_from, recipient_list):
    send_mail(subject, message, email_from, recipient_list)

@shared_task
def send_activation_code_async(email_to, code):
    path = reverse('activate', args=(code, ))
    send_mail(
        'Your activation code',
        f'http://0.0.0.0:8001{path}',
        settings.EMAIL_HOST_USER,
        [email_to],
        fail_silently=False,
    )