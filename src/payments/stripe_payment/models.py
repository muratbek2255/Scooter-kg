from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class StripeWallet(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="stripe_wallet", verbose_name='Wallet'
    )
    balance = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Wallet of {self.owner} with {self.balance}"


class Transaction(models.Model):
    types = (
        ('платеж получен', 'платеж получен'),
        ('платеж сделан', 'платеж сделан'),
        ('платеж снят', 'платеж снят'),
        ('платеж заполнен', 'платеж заполнен')
    )

    wallet = models.ForeignKey(
        StripeWallet, related_name='stripe_transactions', on_delete=models.CASCADE, verbose_name='Wallet'
    )

    email = models.CharField(max_length=128, blank=False, null=False)
    type = models.CharField(max_length=64, choices=types, default='payment_made')
    date = models.DateField(auto_now_add=True, verbose_name='Dates')
    value = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.type} by {self.wallet.owner.email} in amount {self.value} to {self.email} on {self.date}"
