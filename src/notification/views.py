from rest_framework import viewsets, permissions

from src.notification.models import (
    InAppMessage, MobileNotification
)
from src.notification.serializers import (
   InAppMessageSerializer, MobileNotificationSerializer
)


class InAppDeviceViewSet(viewsets.ModelViewSet):
    queryset = InAppMessage.objects.all()
    serializer_class = InAppMessageSerializer
    permission_classes = [permissions.IsAdminUser, ]


class MobileNotificationDeviceViewSet(viewsets.ModelViewSet):
    queryset = MobileNotification.objects.all()
    serializer_class = MobileNotificationSerializer
    permission_classes = [permissions.IsAdminUser, ]
