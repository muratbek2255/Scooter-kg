from django.contrib.auth import get_user_model
from django.db import models

from src.scooter.models import Scooter
from src.user.models import AbstractTimeStampModel as TimestampedModel

User = get_user_model()


class CartItem(TimestampedModel):
    """
    Объект товара в корзине
    """
    product = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Cart(TimestampedModel):
    """
    Обьект корзины
    """

    owner = models.OneToOneField(
        User,
        null=True,
        related_name='user_carts',
        on_delete=models.CASCADE
    )

    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, ("Открыто - в настоящее время активно")),
        (MERGED, ("Объединено - заменено другой корзиной")),
        (SAVED, ("Сохранено - для товаров, которые будут приобретены позже")),
        (FROZEN, ("Заморожено - корзину нельзя изменить")),
        (SUBMITTED, ("Отправлено - заказано на кассе")),
    )

    status = models.CharField(max_length=128, default=OPEN, choices=STATUS_CHOICES)
    merged_date = models.DateTimeField(null=True, blank=True)
    editable_statuses = (OPEN, SAVED)
    items = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return self.owner and self.status
