from django.core.mail import send_mail

from django.conf import settings
from config.celery import app


@app.task
def send_order_info(email, message):
    send_mail(
        'Order info',
        message,
        settings.EMAIL_HOST_USER,
        [email, ],
        fail_silently=False
    )
