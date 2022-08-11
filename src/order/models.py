from django.contrib.auth import get_user_model
from django.db import models

from src.user.models import AbstractTimeStampModel as TimestampedModel
from src.cart.models import Cart, CartItem

User = get_user_model()


class ShippingAddress(TimestampedModel):
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=255)
    notes = models.TextField(blank=True, help_text="Расскажите нам все, что мы должны знать при доставке вашего заказа.")
    address = models.CharField(verbose_name="Адрес доставки", max_length=127)


class Order(TimestampedModel):
    number = models.CharField(verbose_name="Номер заказа", max_length=128, db_index=True, unique=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")
    user = models.ForeignKey(
        User,
        null=True,
        related_name='orders',
        on_delete=models.SET_NULL
    )
    currency = models.CharField(verbose_name="Валюта", max_length=12, default='KG')
    total_prices = models.DecimalField(verbose_name="Общий цены заказа", decimal_places=2, max_digits=12)

    INITIATED, CONFIRMED, SHIPPED, DELIVERED, CANCELED = (
        "инициированный", "подтвержденный", "отправленный", "доставлен", "отменен"
    )
    STATUS = [
        (INITIATED, 'инициированный'),
        (CONFIRMED, "потвержденный"),
        (SHIPPED, "отправленный"),
        (DELIVERED, "доставлен"),
        (CANCELED, "отменен")
    ]
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default=INITIATED, choices=STATUS)


class OrderItem(TimestampedModel):
    number = models.CharField(verbose_name="Номер заказа продукта", max_length=128, db_index=True, unique=True, blank=True)
    seller = models.ForeignKey(
        User,
        null=True,
        related_name='order_items',
        on_delete=models.SET_NULL
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=12, default='KG')
    payment_intent_id = models.CharField(max_length=255, default=None, blank=True, null=True)
    INITIATED, CONFIRMED, SHIPPED, DELIVERED, CANCELED = (
        "инициированный", "подтвержденный", "отправленный", "доставлен", "отменен"
    )
    STATUS = [
        (INITIATED, 'инициированный'),
        (CONFIRMED, "потвержденный"),
        (SHIPPED, "отправленный"),
        (DELIVERED, "доставлен"),
        (CANCELED, "отменен")
    ]
    status = models.CharField(max_length=100, default=INITIATED, choices=STATUS)
