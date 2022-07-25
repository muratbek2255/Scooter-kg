from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from src.user.services import EmailThread

User = get_user_model()


@shared_task
def send_email(site, user):
    user = User.objects.get(user_id=user)

    user = user.email
    current_site = site
    subject = 'Активируйте свой аккаунт'
    message = render_to_string('emails/activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    })

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    EmailThread(message).start()
