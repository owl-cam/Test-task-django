from django.db import models


class EventPlace(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    long = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Долгота")
    lat = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Широта")

    class Meta:
        verbose_name = "Место проведения"
        verbose_name_plural = "Места проведения"

    def __str__(self) -> str:
        return str(self.name)
