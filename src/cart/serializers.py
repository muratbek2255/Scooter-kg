from rest_framework import fields, serializers
from src.cart.models import Cart, CartItem
from src.scooter.serializers import ScooterPublicSerializer


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "created_at",
            "updated_at",
        ]


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = [
            "id",
            "owner",
            "status",
            "merged_date",
            "items",
            "created_at",
            "updated_at",
        ]
