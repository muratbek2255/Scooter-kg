from django.core.exceptions import ObjectDoesNotExist
from src.wallets.stripe_wallets.models import StripeWallet


class WalletController(object):
    def get(self, owner):
        try:
            wallet = StripeWallet.objects.get(owner=owner)
        except ObjectDoesNotExist:
            wallet = StripeWallet.objects.create(owner=owner)

        return wallet
