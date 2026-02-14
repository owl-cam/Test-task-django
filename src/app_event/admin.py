from django.contrib import admin

from .models import Event, EventImage


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "published",
        "author",
        "place",
        "rate",
        "start_date",
        "end_date",
    )
    list_filter = ("status", "published", "place")
    search_fields = ("name", "author", "description")
    list_editable = ("published", "status")
    date_hierarchy = "start_date"
    inlines = [EventImageInline]
    fieldsets = (
        (
            None,
            {
                "fields": ("published", "name", "description", "author"),
            },
        ),
        (
            "Даты",
            {
                "fields": ("publish_date", "start_date", "end_date"),
            },
        ),
        (
            "Параметры",
            {
                "fields": ("place", "rate", "status"),
            },
        ),
    )
