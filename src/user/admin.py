from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from src.user.models import User


@admin.register(User)
class UserAdmin(TranslationAdmin):
    pass
