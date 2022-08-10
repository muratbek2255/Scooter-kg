from django.db.models.signals import post_save
from django.dispatch import receiver

from src.notification.tasks import send_new_message_push_notification
from src.notification.models import InAppMessage


@receiver(post_save, sender=InAppMessage)
def send_new_message_notification(sender, **kwargs):
    message = kwargs['instance']
    send_new_message_push_notification.delay(sender_id=message.sender.id,
                                             recipient_id=message.recipient.id,
                                             content=message.content)
