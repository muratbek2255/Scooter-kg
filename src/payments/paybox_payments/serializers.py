from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.db.models import F
from rest_framework import serializers

from decimal import Decimal

from .models import Transaction, PayboxWallet

User = get_user_model()


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayboxWallet
        fields = (
            'id', 'owner', 'balance'
        )


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value',)

    def create(self, **validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def save(self, **validated_data):
        user = User.objects.get(pk=validated_data['owner'].id)
        wallet = user.wallet
        wallet.balance = F('balance') + Decimal(self.initial_data['value'])
        wallet.save(update_fields=['balance'])
        transaction = Transaction.objects.create(wallet=wallet,
                                                 email=user.email,
                                                 type='payment_fill',
                                                 value=Decimal(self.initial_data['value']))
        return transaction

    @staticmethod
    def validate_value(value):
        if Decimal(value) <= 0:
            raise serializers.ValidationError("Вы должны заполнить кошелек на сумму больше 0")


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value',)

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def save(self, **validated_data):
        user = User.objects.get(pk=validated_data['owner'].id)
        wallet = user.wallet
        if wallet.balance < Decimal(self.initial_data['value']):
            raise serializers.ValidationError("Извините, у вас недостаточно денег в кошельке")
        wallet.balance = F('balance') - Decimal(self.initial_data['value'])
        wallet.save(update_fields=['balance'])
        transaction = Transaction.objects.create(wallet=wallet,
                                                 email=user.email,
                                                 type='payment_withdraw',
                                                 value=Decimal(self.initial_data['value']))
        return transaction

    @staticmethod
    def validate_value(value):
        if Decimal(value) <= 0:
            raise serializers.ValidationError("Вы должны заполнить кошелек на сумму больше 0")


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value', 'email',)

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def save(self, **validated_data):
        payer = User.objects.get(pk=validated_data['owner'].id)
        wallet = payer.wallet
        if wallet.balance < Decimal(self.initial_data['value']):
            raise serializers.ValidationError("Извините, у вас недостаточно денег в кошельке")
        else:
            with atomic():
                payer_wallet = payer.wallet
                receiver = User.objects.get(email=self.initial_data['email'])
                receiver_wallet = receiver.wallet

                payer_wallet.balance = F('balance') - Decimal(self.initial_data['value'])
                receiver_wallet.balance = F('balance') + Decimal(self.initial_data['value'])

                payer_wallet.save(update_fields=['balance'])
                receiver_wallet.save(update_fields=['balance'])

                payer_transaction = Transaction.objects.create(
                    wallet=payer_wallet,
                    email=payer.email,
                    type='payment_made',
                    value=Decimal(self.initial_data['value'])
                )

                receiver_transaction = Transaction.objects.create(
                    wallet=receiver_wallet,
                    email=receiver.email,
                    type='payment_received',
                    value=Decimal(self.initial_data['value'])
                )

                payer_transaction.save()
                receiver_transaction.save()

    @staticmethod
    def validate_value(value):
        if Decimal(value) <= 0:
            raise serializers.ValidationError("Вы должны определить значение платежа больше, чем 0")

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email):
            raise serializers.ValidationError(
                "Получателя платежа с таким адресом электронной почты нет. Пожалуйста, проверь это"
            )


class TransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    type = serializers.CharField()
    value = serializers.DecimalField(max_digits=15, decimal_places=2)
