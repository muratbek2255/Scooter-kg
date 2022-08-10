from modeltranslation.translator import register, TranslationOptions
from src.bicycle.models import Bicycle


@register(Bicycle)
class BicycleTranslationOptions(TranslationOptions):
    fields = ('title', 'address')
