from rest_framework.routers import DefaultRouter

from src.notification.views import InAppDeviceViewSet, MobileNotificationDeviceViewSet

router = DefaultRouter()
router.register(r'in-app-devices', InAppDeviceViewSet)
router.register(r'notifications', MobileNotificationDeviceViewSet)

urlpatterns = router.urls
