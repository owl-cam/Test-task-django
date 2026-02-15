from pydantic import BaseModel


class WeatherDomain(BaseModel):
    temp: float
    condition: str
    humidity: int
    pressure: int
    wind_dir: str
    wind_speed: float
