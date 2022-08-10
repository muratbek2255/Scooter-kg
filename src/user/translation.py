from modeltranslation.translator import register, TranslationOptions
from src.user.models import User


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = (
        'email', 'first_name', 'last_name',
        'social_network',
    )
    