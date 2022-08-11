from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import (
    permissions, generics, viewsets,
    views, status
)
from rest_framework.response import Response
from twilio.rest import Client

from src.user.serializers import (
    UserRegistrationSerializer, LoginSerializer, LogOutSerializer,
    UserSerializer, ChangePasswordSerializer, UpdateUserSerializer,
    OtpSerializer, PhoneNumberSerializer, CreateNewPasswordSerializerAfterReset, ResetPasswordEmailRequestSerializer
)
from src.user.services import generate_otp
from src.user.tasks import (
    send_activation_code, send_reset_code
)

User = get_user_model()


class UserAPIViewSet(viewsets.ModelViewSet):
    """Вывод всех пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )


class UserRegistrationView(generics.GenericAPIView):
    """ Регистрация пользователя """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code.delay(email=user.email, activation_code=user.activation_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """Для логина пользователя """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class SendSmsView(generics.GenericAPIView):
    """Отправка на смс код верифифкации"""
    serializer_class = PhoneNumberSerializer
    otp = None

    @transaction.atomic()
    def post(self, request):
        data = request.data
        email = data['email']
        user = User.objects.get(email=email)
        phone_number_valid = PhoneNumberSerializer(data=data)
        if not phone_number_valid.is_valid():
            return Response({'errors': 'Не валидный номер телефона'})

        phone_number = data['phone_number']
        otp = self.otp
        if otp is None:
            otp = generate_otp()

        user.otp_code = otp
        user.phone_number = phone_number
        expiry = timezone.now() + timedelta(minutes=30)
        user.otp_code_expiry = expiry
        user.save()

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message_to_broadcast = f'Твой верификационный код {otp}'
            client.messages.create(to=phone_number,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)

            return Response({'message': 'Код был отправлен', 'otp': otp})
        except Exception as exc:
            print(f'we caucht {exc}')
            print(f'we caucht {type(exc)}')
            return Response({'errors': 'Есть некоторые проблемы с отправкой кода'})


class VerifyOtpView(generics.GenericAPIView):
    """ Активизация через смс """
    serializer_class = OtpSerializer

    def post(self, request):
        data = request.data
        user = User.objects.filter(email=data['email'])

        if not user.exists():
            return Response({'errors': 'Ты не зарегестрирован'})

        user = user[0]

        if user.otp_code != data['otp_code']:
            return Response({'errors': 'Пожайлуста введите валидный код'})

        otp_expired = OtpSerializer(data=data)

        if not otp_expired:
            return Response({'errors': 'Закончился срок годности кода'})

        user.phone_verified = True
        user.save()
        return Response({'message': 'Номер активирован'})


class DeleteAccountAPIView(views.APIView):
    """Удаление пользователя"""
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "Данный пользователь был удален"})


class ActivateView(views.APIView):
    """Активация кода через эл.почту"""
    def get(self, request, activation_code):
        user = User()
        user.is_active = True
        user.activation_code = activation_code
        user.save()
        return Response('Your account successfully activated!', status=status.HTTP_200_OK)


class ForgotPassword(generics.GenericAPIView):
    """ Отправка на эл.почту для сброса пароля """

    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = ResetPasswordEmailRequestSerializer(data=request.data)
        email = request.query_params.get('email')

        if User.objects.filter(email=email).exists():
            user = request.user
            user.is_active = False
            user.create_activation_code()
            user.save()
            print(user)
            send_reset_code.delay(email=user.email, activation_code=user.activation_code)
            return Response("Вам отправили сообщение", status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'Could not password, invalid token'}, status.HTTP_400_BAD_REQUEST)


class ForgotPasswordComplete(views.APIView):
    """ Создание пароля после сброса через эл.почту """
    def post(self, request):
        serializer = CreateNewPasswordSerializerAfterReset(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=200)


def auth(request):
    """ Для авторизации через гитхаб """
    return render(request, 'github_authentication.html')
