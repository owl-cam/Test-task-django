from celery import shared_task
from django.conf import settings
from requests import get

from app_event_place.models import EventPlace

from .models import Weather


@shared_task
def update_weather():
    for place in EventPlace.objects.all():
        weather = Weather.objects.filter(pk=place.id).first()
        if not weather:
            weather = Weather(place=place)
        data = get(
            "https://api.weatherapi.com/v1/current.json",
            params={
                "lang": "ru",
                "q": f"{place.long},{place.lat}",
                "key": settings.WEATHER_API_KEY,
            },
        )
        if data.status_code != 200:
            continue
        json_data = data.json()["current"]
        weather.condition = json_data["condition"]["text"]
        weather.humidity = json_data["humidity"]
        weather.pressure = json_data["pressure_mb"]
        weather.temp = json_data["temp_c"]
        weather.wind_dir = json_data["wind_dir"]
        weather.wind_speed = json_data["wind_kph"]
        weather.save()
