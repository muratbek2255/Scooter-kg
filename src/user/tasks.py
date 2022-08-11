from django.core.mail import send_mail

from django.conf import settings
from config.celery import app


@app.task
def send_activation_code(email, activation_code):
    activation_url = f'https://4977-212-42-120-155.in.ngrok.io/ru/api/v1/activate/{activation_code}/'
    message = f"""
        Thank you for signing up.
        Please, activate your account.
        Activation link: {activation_url}
    """
    send_mail(
        'Activate your account',
        message,
        settings.EMAIL_HOST_USER,
        [email, ],
        fail_silently=True
    )


@app.task
def send_reset_code(email, activation_code):
    message = f"""
        Activation code: {activation_code}
    """
    send_mail(
        'Reset your password',
        message,
        settings.EMAIL_HOST_USER,
        [email, ],
        fail_silently=False
    )
