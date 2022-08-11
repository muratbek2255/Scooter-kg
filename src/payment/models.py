from django.db import models
from src.user.models import AbstractTimeStampModel as TimestampedModel
from src.order.models import Order


class PaymentModel(TimestampedModel):
    order_number = models.OneToOneField(Order, to_field='number', on_delete=models.CASCADE)
    method = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=12, default='EUR')
    OPEN, DONE = (
        "open", 'done'
    )
    STATUS = [
        (OPEN, "open"),
        (DONE, "done")
    ]
    status = models.CharField(max_length=100, default=OPEN, choices=STATUS)
