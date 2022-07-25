from django.urls import path

from src.user.views import (
    UserRegistrationView, UserLoginView, UserLoginOutView,
    UserAPIViewSet, ChangePasswordView, UpdateProfileView
)

urlpatterns = [
    path('users/', UserAPIViewSet.as_view({'get': 'list'})),
    path('user/<int:pk>/', UserAPIViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('register/', UserRegistrationView.as_view(), name='auth_register'),
    path('login/', UserLoginView.as_view(), name='auth_login'),
    path('logout/', UserLoginOutView.as_view(), name='auth_logout'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
]
