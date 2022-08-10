from rest_framework.routers import DefaultRouter

from src.bicycle.views import BicyclePublicViewSet

router = DefaultRouter()
router.register(r'bicycles', BicyclePublicViewSet)

urlpatterns = router.urls
