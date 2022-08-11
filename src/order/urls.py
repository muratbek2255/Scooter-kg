from rest_framework import routers
from src.order import views

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)

urlpatterns = router.urls
