from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions, generics, viewsets

from src.user.serializers import (
    UserRegistrationSerializer, LoginSerializer, LogOutSerializer,
    UserSerializer, ResetPasswordOnEmailRequestSerializer, ChangePasswordSerializer, UpdateUserSerializer
)

User = get_user_model()


class UserAPIViewSet(viewsets.ModelViewSet):
    """Вывод всех пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )


class UserRegistrationView(generics.CreateAPIView):
    """ Регистрация пользователя """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny, )


class UserLoginView(generics.CreateAPIView):
    """ Логин пользователя """
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny, )


class UserLoginOutView(generics.CreateAPIView):
    """ Выход из приложения пользователя """
    queryset = User.objects.all()
    serializer_class = LogOutSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChangePasswordView(generics.UpdateAPIView):
    """Обновление пароля пользователя"""
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    """Обновление профиля пользователя"""
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UpdateUserSerializer


class RequestPasswordResetOnEmail(generics.GenericAPIView):
    """Сброс пароля"""
    serializer_class = ResetPasswordOnEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)


def auth(request):
    return render(request, 'github_authentication.html')
