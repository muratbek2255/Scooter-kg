from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from src.bicycle.models import Bicycle, RatingBicycleRelation


@admin.register(Bicycle)
class BicycleAdmin(TranslationAdmin):
    pass


@admin.register(RatingBicycleRelation)
class RatingBicycleAdmin(admin.ModelAdmin):
    pass
