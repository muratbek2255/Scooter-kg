from rest_framework import serializers

from src.scooter.models import Scooter, RatingScooterRelation


class ScooterPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scooter
        fields = (
            'id', 'title', 'price', 'battery',
            'mileage', 'image', 'address',
            'code', 'qr_code', 'quantity'
        )
        extra_kwargs = {
            'code': {'read_only': True},
            'qr_code': {'read_only': True},
        }


class ScooterRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingScooterRelation
        fields = ('user', 'scooter', 'rate')
