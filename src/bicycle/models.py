from django.contrib.auth import get_user_model
from django.db import models

from src.user.models import AbstractTimeStampModel

User = get_user_model()


class Bicycle(AbstractTimeStampModel):
    """ Модель для велосипеда """
    title = models.CharField("Название", max_length=127)
    price = models.IntegerField("Цена", default=0)
    image = models.ImageField("Картинка", upload_to='./scooters')
    code = models.CharField(
        "КОд", max_length=255,
        blank=True, null=False, unique=True, default='1HHN89FD'
    )
    address = models.CharField(
        "Адрес самоката", max_length=255,
        blank=True, null=True
    )
    qr_code = models.ImageField("Qr code самоката", upload_to='./qr_codes')\


    @property
    def overall_rating(self):
        ratings = RatingBicycleRelation.objects.filter(scooter=self.id)
        if len(ratings) > 0:
            return sum([x.rating for x in ratings]) / len(ratings)
        else:
            return 0

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'bicycles'
        verbose_name = 'Bicycle'
        verbose_name_plural = 'Bicycles'


class RatingBicycleRelation(AbstractTimeStampModel):
    """ Рейтинг велосипедов """
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(
        verbose_name="Пользователь", to=User, on_delete=models.CASCADE,
        blank=True, null=False, related_name='rating_users',default=1
    )
    bicycle = models.ForeignKey(
        verbose_name="Велосипед", to=Bicycle, on_delete=models.CASCADE,
        blank=True, null=False, related_name='rating_bicycles', default=1
    )
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f' {self.user_id}: {self.bicycle_id}, RATE {self.rate}'

    class Meta:
        db_table = 'rating_bicycles'
        verbose_name = 'Rating_bicycle'
        verbose_name_plural = 'Rating_bicycles'
