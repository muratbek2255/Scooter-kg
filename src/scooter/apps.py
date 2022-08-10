from django.apps import AppConfig


class ScooterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.scooter'

    def ready(self):
        import src.scooter.signals
