from datetime import datetime

from ninja import Schema
from pydantic.types import constr

from app_event_place.schema import EventPlaceSchema

from .domain import EventCreateDomain, EventFilterDomain, EventStatus, EventUpdateDomain

id_list_type = constr(strip_whitespace=True, pattern=r"^[0-9|,]+$")


class EventSchema(Schema):
    id: int
    published: bool
    name: str
    description: str
    publish_date: datetime | None
    start_date: datetime
    end_date: datetime
    author: str
    place: EventPlaceSchema | None = None
    rate: int
    status: EventStatus


class EventListSchema(Schema):
    data: list[EventSchema]
    total: int
    limit: int
    offset: int


class EventCreateSchema(Schema):
    published: bool
    name: str
    description: str
    publish_date: datetime | None = None
    start_date: datetime
    end_date: datetime
    author: str
    place_id: int | None = None
    rate: int
    status: EventStatus

    def to_domain(self) -> EventCreateDomain:
        return EventCreateDomain(**self.dict(exclude_unset=True))


class EventUpdateSchema(Schema):
    published: bool | None = None
    name: str | None = None
    description: str | None = None
    publish_date: datetime | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    author: str | None = None
    place_id: int | None = None
    rate: int | None = None
    status: EventStatus | None = None

    def to_domain(self) -> EventUpdateDomain:
        return EventUpdateDomain(**self.dict(exclude_unset=True))


class EventFilterSchema(Schema):
    published: bool | None = None
    start_date_gte: datetime | None = None
    start_date_lte: datetime | None = None
    end_date_gte: datetime | None = None
    end_date_lte: datetime | None = None
    place_id_in: id_list_type | None = None
    rate_gte: int | None = None
    rate_lte: int | None = None
    query: str | None = None

    def to_domain(self) -> EventFilterDomain:
        return EventFilterDomain(
            place_id_in=self.place_id_in.split(",") if self.place_id_in else None,
            **self.dict(exclude_unset=True, exclude={"place_id_in"}),
        )


class EventExportFilterSchema(Schema):
    publish_date_gte: datetime | None = None
    publish_date_lte: datetime | None = None
    start_date_gte: datetime | None = None
    start_date_lte: datetime | None = None
    end_date_gte: datetime | None = None
    end_date_lte: datetime | None = None
    place_id: int | None = None
    rate_gte: int | None = None
    rate_lte: int | None = None


class ImportRowError(Schema):
    row: int
    field: str
    error: str
    value: str | None = None


class ImportResultSchema(Schema):
    success: bool
    total_rows: int
    imported_count: int
    errors: list[ImportRowError]
    created_places: list[str]
