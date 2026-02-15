from django.db import models


class Weather(models.Model):
    place = models.OneToOneField(
        to="app_event_place.EventPlace", on_delete=models.CASCADE, primary_key=True
    )
    temp = models.FloatField()
    condition = models.CharField(max_length=100)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_dir = models.CharField(max_length=10)
    wind_speed = models.FloatField()
