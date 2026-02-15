from django.db.models.signals import pre_save
from django.dispatch import receiver

from app_event.models import Event


@receiver(pre_save, sender=Event)
def send_email_on_publish(sender, instance, **kwargs):
    if not instance.published:
        return

    if instance.pk:
        if old := Event.objects.filter(pk=instance.pk).first():
            if old.published:
                return

    from constance import config
    from django.template.loader import render_to_string
    from post_office import mail

    recipients = [e.strip() for e in config.EMAIL_TO.split(",") if e.strip()]
    if not recipients:
        return

    html_message = render_to_string(
        "app_event/email/new_event.html",
        {"event": instance, "email_text": config.EMAIL_TEXT},
    )

    mail.send(
        recipients,
        subject=config.EMAIL_SUBJECT,
        html_message=html_message,
    )
