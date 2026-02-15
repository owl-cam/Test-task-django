from pydantic import BaseModel

from app_weather.domain import WeatherDomain


class EventPlaceDomain(BaseModel):
    id: int
    name: str
    long: float
    lat: float
    weather: WeatherDomain | None = None
