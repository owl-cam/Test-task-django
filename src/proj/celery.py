import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")

app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.autodiscover_tasks(["app_weather", "app_event"], related_name="task")


@app.task
def send_queued_emails():
    from post_office import mail

    mail.send_queued()


app.conf.beat_schedule = {
    "send-queued-emails": {
        "task": "proj.celery.send_queued_emails",
        "schedule": 300,  # every 5 minutes
    },
    "update-weather": {
        "task": "app_weather.task.update_weather",
        "schedule": 3600,  # every hour
    },
    "publish-scheduled-events": {
        "task": "app_event.task.publish_scheduled_events",
        "schedule": 300.0,  # every 5 minutes
    },
}
