from rest_framework.routers import DefaultRouter

from src.scooter.views import ScooterPublicViewSet

router = DefaultRouter()
router.register(r'scooters', ScooterPublicViewSet)

urlpatterns = router.urls
