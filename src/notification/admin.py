from django.contrib import admin

from src.notification.models import InAppMessage, MobileNotification


@admin.register(InAppMessage)
class InAppMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(MobileNotification)
class InAppMessageAdmin(admin.ModelAdmin):
    pass
