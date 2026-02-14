from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Event(models.Model):
    SOON = "soon"
    ONGOING = "ongoing"
    OVER = "over"

    published = models.BooleanField(verbose_name="Опубликовано", default=True)
    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    publish_date = models.DateTimeField(
        verbose_name="Дата публикации", null=True, blank=True
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    author = models.CharField(max_length=250, verbose_name="Автор")
    place = models.ForeignKey(
        to="app_event_place.EventPlace",
        on_delete=models.SET_NULL,
        related_name="events",
        verbose_name="Место проведения",
        null=True,
        blank=True,
    )
    rate = models.SmallIntegerField(
        verbose_name="Рейтинг",
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        help_text="От 0 до 25",
    )
    status = models.CharField(
        choices=[(SOON, "Скоро"), (ONGOING, "Идет"), (OVER, "Закончилось")],
        max_length=10,
        default=SOON,
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self) -> str:
        return str(self.name)


class EventImage(models.Model):
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Мероприятие",
    )
    image = models.ImageField(upload_to="event", verbose_name="Изображение")
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFit(200, 200)],
        format="JPEG",
        options={"quality": 80},
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
