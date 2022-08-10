from django.urls import path

from src.user.views import (
    UserRegistrationView, UserLoginView, UserLoginOutView,
    UserAPIViewSet, ChangePasswordView, UpdateProfileView,
    SendSmsView, VerifyOtpView, DeleteAccountAPIView,
    ActivateView, ForgotPassword, ForgotPasswordComplete,
)

urlpatterns = [
    path('users/', UserAPIViewSet.as_view({'get': 'list'})),
    path('user/<int:pk>/', UserAPIViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('register/', UserRegistrationView.as_view(), name='auth_register'),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', UserLoginView.as_view(), name='auth_login'),
    path('logout/', UserLoginOutView.as_view(), name='auth_logout'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('forgot_password/', ForgotPassword.as_view()),
    path('forgot_password_complete/', ForgotPasswordComplete.as_view()),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('delete_profile/<int:pk>/', DeleteAccountAPIView.as_view(), name='delete_profile'),
    path('send-sms/', SendSmsView.as_view(), name='send-sms'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp')
]
