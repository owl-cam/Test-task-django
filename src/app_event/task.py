from celery import shared_task
from django.utils import timezone


@shared_task
def publish_scheduled_events():
    from app_event.models import Event

    now = timezone.now()
    events = Event.objects.filter(published=False, publish_date__lte=now)
    count = events.count()
    for event in events:
        event.published = True
        event.save()  # triggers pre_save signal → email queued
    return f"Published {count} events"
