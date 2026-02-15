from ninja import Schema

from app_weather.schema import WeatherSchema


class EventPlaceSchema(Schema):
    id: int
    name: str
    long: float
    lat: float
    weather: WeatherSchema | None = None


class EventPlaceListSchema(Schema):
    data: list[EventPlaceSchema]
    total: int
    limit: int
    offset: int


class EventPlaceCreateSchema(Schema):
    name: str
    long: float
    lat: float


class EventPlaceUpdateSchema(Schema):
    name: str | None = None
    long: float | None = None
    lat: float | None = None
