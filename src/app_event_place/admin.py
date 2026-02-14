from django.contrib import admin

from .models import EventPlace


@admin.register(EventPlace)
class EventPlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "lat", "long")
    search_fields = ("name",)
