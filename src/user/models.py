from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from src.user.managers import UserManager


class AbstractTimeStampModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractUser):
    """Кастомный пользователь"""
    email = models.EmailField('Электронная почта', unique=True)
    first_name = models.CharField('Имя', max_length=125)
    last_name = models.CharField('Фамилия', max_length=125)
    social_network = models.URLField(
        'Социальная сеть', max_length=200,
        blank=True, null=True, default=AUTH_PROVIDERS.get('email'))
    phone_number = models.CharField("Номер телефона", max_length=127, unique=True)
    otp_code = models.CharField("Код верификации по номеру телефона", max_length=30, null=True)
    otp_code_expiry = models.DateTimeField("Срок годности кода", default=timezone.now)
    activation_code = models.CharField("Код для верификации по емайлу", max_length=58, blank=True)

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def create_activation_code(self):
        code = get_random_string(6, allowed_chars='123456789')
        self.activation_code = code

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'id: {self.id}, email: {self.email}'

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
