from rest_framework import serializers

from src.notification.models import (
    InAppMessage, MobileNotification
)


class MobileNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileNotification
        fields = ('recipient', 'title', 'message', 'status')


class InAppMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InAppMessage
        fields = ('sender', 'recipient', 'content')
