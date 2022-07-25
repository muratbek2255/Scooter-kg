from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from src.user.managers import UserManager


class AbstractTimeStampModel(models.Model):

    first_login = models.DateTimeField(auto_now_add=True)
    updated_login = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractUser):
    """Кастомный пользователь"""
    email = models.EmailField('Электронная почта', unique=True)
    first_name = models.CharField('Имя', max_length=125)
    last_name = models.CharField('Фамилия', max_length=125)
    phone_number = models.PositiveBigIntegerField('Номер телефона', unique=True,default='+996000000000')
    social_network = models.URLField(
        'Социальная сеть', max_length=200,
        blank=True, null=True, default=AUTH_PROVIDERS.get('email'))
    is_verifed = models.BooleanField("Прошел верикацию", default=False)
    balance = models.PositiveIntegerField(default=0)

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'id: {self.id}, email: {self.email}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']
