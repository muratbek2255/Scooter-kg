from rest_framework import serializers

from src.bicycle.models import (
    Bicycle, RatingBicycleRelation
)


class BicyclePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bicycle
        fields = (
            'id', 'title', 'price',
            'image', 'address', 'code', 'qr_code'
        )
        extra_kwargs = {
            'code': {'read_only': True},
            'qr_code': {'read_only': True},
        }


class BicycleRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingBicycleRelation
        fields = (
            'user', 'bicycle', 'rate'
        )
