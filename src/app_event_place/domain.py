from pydantic import BaseModel


class EventPlaceDomain(BaseModel):
    id: int
    name: str
    long: float
    lat: float
