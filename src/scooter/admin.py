from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from src.scooter.models import Scooter, RatingScooterRelation


@admin.register(Scooter)
class ScooterAdmin(TranslationAdmin):
    pass


@admin.register(RatingScooterRelation)
class RatingScooterAdmin(admin.ModelAdmin):
    pass

