from django.apps import AppConfig


class StripePaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.payments.stripe_payment'
