from ninja import Query, Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from app_event.domain import EventOrder
from app_event.service import EventService

from .schema import (
    EventCreateSchema,
    EventFilterSchema,
    EventListSchema,
    EventSchema,
    EventUpdateSchema,
)

event_router_v1 = Router(tags=["event"], auth=JWTAuth())

service = EventService()


@event_router_v1.get("/{id}", response=EventSchema)
def get_by_id(request, id: int):
    return service.get_by_id(request.user, item_id=id)


@event_router_v1.get("", response=EventListSchema)
def get_list(
    request,
    filters: Query[EventFilterSchema],
    limit=20,
    offset=0,
    order: EventOrder | None = None,
):
    return service.get_list(request.user, limit, offset, filters.to_domain(), order)


@event_router_v1.post("", response=EventSchema)
def create(request, data: EventCreateSchema):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")
    return service.create(data.to_domain())


@event_router_v1.patch("/{id}", response=EventSchema)
def update(request, id: int, data: EventUpdateSchema):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")
    return service.update(id, data.to_domain())


@event_router_v1.delete("/{id}", response={204: None})
def delete(request, id: int):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")
    return service.delete(id)
