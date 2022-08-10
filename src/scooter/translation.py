from modeltranslation.translator import register, TranslationOptions
from src.scooter.models import Scooter


@register(Scooter)
class BicycleTranslationOptions(TranslationOptions):
    fields = ('title', 'address')
