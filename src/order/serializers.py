from rest_framework import fields, serializers

from src.cart.models import Cart
from src.cart.serializers import CartItemSerializer, CartSerializer
from src.order.models import Order, OrderItem, ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "phone_number",
            "notes",
            "address",
            "created_at",
            "updated_at",
        ]


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "number",
            "order",
            "payment_intent_id",
            "cart_item",
            "amount",
            "status",
            "currency",
            "created_at",
            "updated_at",
        ]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "id",
            "number",
            "cart",
            "user",
            "currency",
            "total_prices",
            "shipping_address",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderDetailsSerializer(serializers.ModelSerializer):\

    class Meta:
        model = Order
        fields = [
            "id",
            "number",
            "cart",
            "order_items",
            "user",
            "currency",
            "total_prices",
            "shipping_address",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderItemDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "number",
            "payment_intent_id",
            "order",
            "cart_item",
            "amount",
            "status",
            "currency",
            "created_at",
            "updated_at",
        ]
