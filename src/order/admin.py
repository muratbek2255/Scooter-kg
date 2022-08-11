from django.contrib import admin

from src.order.models import (
    ShippingAddress, Order
)

admin.site.register(ShippingAddress)
admin.site.register(Order)
