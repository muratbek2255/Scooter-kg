from django.contrib import admin

from src.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
