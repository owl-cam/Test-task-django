from ninja import Schema


class EventPlaceSchema(Schema):
    id: int
    name: str
    long: float
    lat: float


class EventPlaceListSchema(Schema):
    data: list[EventPlaceSchema]
    total: int


class EventPlaceCreateSchema(Schema):
    name: str
    long: float
    lat: float


class EventPlaceUpdateSchema(Schema):
    name: str | None = None
    long: float | None = None
    lat: float | None = None
