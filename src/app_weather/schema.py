from ninja import Schema


class WeatherSchema(Schema):
    temp: float
    condition: str
    humidity: int
    pressure: int
    wind_dir: str
    wind_speed: float
