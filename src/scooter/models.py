from django.contrib.auth import get_user_model
from django.db import models

from src.user.models import AbstractTimeStampModel

User = get_user_model()


class Scooter(AbstractTimeStampModel):
    """Самокаты"""
    title = models.CharField("Название самоката", max_length=127)
    price = models.IntegerField("Цена за самокат", default=0)
    battery = models.IntegerField("Батарейка самоката", default=0)
    mileage = models.IntegerField("Километраж самоката", default=0)
    image = models.ImageField("Картинка самокатов", upload_to='./scooters')
    quantity = models.IntegerField()
    code = models.CharField(
        "Номер самоката", max_length=255,
        blank=True, null=False, unique=True, default='1HHN89FD'
    )
    address = models.CharField(
        "Адрес самоката", max_length=255,
        blank=True, null=True
    )
    qr_code = models.ImageField("Qr code самоката", upload_to='./qr_codes')

    @property
    def overall_rating(self):
        ratings = RatingScooterRelation.objects.all().filter(book=self.id)
        if len(ratings) > 0:
            return sum([x.rating for x in ratings]) / len(ratings)
        else:
            return 0

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'scooters'
        verbose_name = 'Scooter'
        verbose_name_plural = 'Scooters'


class RatingScooterRelation(AbstractTimeStampModel):
    """ Рейтинг самокатов """
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(
        verbose_name="Пользователь", to=User, on_delete=models.CASCADE,
        blank=True, null=False, related_name='rating_users_2', default=1
    )
    scooter = models.ForeignKey(
        verbose_name="Самокат", to=Scooter, on_delete=models.CASCADE,
        blank=True, null=False, related_name='rating_scooters', default=1
    )
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f' {self.user}: {self.scooter}, RATE {self.rate}'

    class Meta:
        db_table = 'rating_scooters'
        verbose_name = 'Rating_scooter'
        verbose_name_plural = 'Rating_scooters'
