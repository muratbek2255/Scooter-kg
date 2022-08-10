from django.contrib.auth import get_user_model
from django.db import models

from src.user.models import AbstractTimeStampModel


User = get_user_model()


class MobileNotification(AbstractTimeStampModel):
    recipient = models.ForeignKey(User, related_name='user_device_notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=512, null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=10, default='unread')


class InAppMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
