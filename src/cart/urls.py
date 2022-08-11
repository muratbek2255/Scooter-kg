from rest_framework import routers
from src.cart import views

router = routers.DefaultRouter()
router.register(r'carts', views.CartViewSet)
router.register(r'cart_items', views.CartItemViewSet)

urlpatterns = router.urls
