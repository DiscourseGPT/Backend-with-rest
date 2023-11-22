from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from requests import request


def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    html_message = render_to_string('email_template.html', {'token': token})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email = EmailMultiAlternatives(subject, plain_message, email_from, recipient_list)
    email.attach_alternative(html_message, 'text/html')
    email.send()

    return True
