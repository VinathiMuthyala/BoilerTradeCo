# django-email-server.py
from django.core.mail import send_mail
from django.conf import settings

def send(subject, message, recipients):
    send_mail( subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipients)