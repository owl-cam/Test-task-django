from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from app_event_place.domain import EventPlaceDomain


class EventStatus(str, Enum):
    SOON = "soon"
    ONGOING = "ongoing"
    OVER = "over"


class EventOrder(str, Enum):
    NAME = "name"
    STARTDATE = "start_date"
    ENDDATE = "end_date"


class EventDomain(BaseModel):
    id: int
    published: bool
    name: str
    description: str
    publish_date: datetime | None = None
    start_date: datetime
    end_date: datetime
    author: str
    place_id: int | None = None
    place: EventPlaceDomain | None = None
    rate: int
    status: EventStatus


class EventListDomain(BaseModel):
    data: list[EventDomain]
    total: int
    limit: int
    offset: int


class EventCreateDomain(BaseModel):
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


class EventUpdateDomain(BaseModel):
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


class EventFilterDomain(BaseModel):
    id: int | None = None
    published: bool | None = None
    start_date_gte: datetime | None = None
    start_date_lte: datetime | None = None
    end_date_gte: datetime | None = None
    end_date_lte: datetime | None = None
    place_id_in: list[int] | None = None
    rate_gte: int | None = None
    rate_lte: int | None = None
    query: str | None = None
