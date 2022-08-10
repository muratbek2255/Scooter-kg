from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from pyfcm import FCMNotification

from src.notification.models import MobileNotification

User = get_user_model()


@shared_task
def send_new_message_push_notification(**kwargs):
    sender = User.objects.get(id=kwargs.get("sender_id"))
    recipient = User.objects.get(id=kwargs.get("recipient_id"))
    content = kwargs.get("content")
    notification = MobileNotification()
    notification.recipient = recipient
    notification.title = "New notification"
    sender_full_name = "{} {}".format(sender.first_name,
                                      sender.last_name)
    message = '{} has sent you a message: "{}"'.format(sender_full_name,
                                                       content)
    notification.message = message

    if recipient.has_android_device():
        data_payload = {
            "badge": recipient.unread_notifications_count(),
            "alert": notification.title,
            "notification_id": notification.pk,
            "body": notification.message,
        }
        fcm = FCMNotification(api_key=settings.FIREBASE_API_KEY)

        return fcm.notify_single_device(
            registration_id=str(recipient.device.token),
            badge=recipient.unread_notifications_count(),
            data_message=data_payload,
            message_body=content)
