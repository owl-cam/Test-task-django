from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from app_event_place.models import EventPlace

from .schema import (
    EventPlaceCreateSchema,
    EventPlaceListSchema,
    EventPlaceSchema,
    EventPlaceUpdateSchema,
)

event_place_router_v1 = Router(tags=["event_place"], auth=JWTAuth())


def _require_superuser(request):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")


@event_place_router_v1.get("/{id}", response=EventPlaceSchema)
def get_by_id(request, id: int):
    _require_superuser(request)
    return get_object_or_404(EventPlace, pk=id)


@event_place_router_v1.get("", response=EventPlaceListSchema)
def get_all(request, offset: int = 0, limit: int = 20):
    _require_superuser(request)
    return EventPlaceListSchema(
        data=EventPlace.objects.all()[offset : limit + offset],
        total=EventPlace.objects.count(),
        limit=limit,
        offset=offset,
    )


@event_place_router_v1.post("", response=EventPlaceSchema)
def create(request, data: EventPlaceCreateSchema):
    _require_superuser(request)
    res = EventPlace(**data.dict())
    res.save()
    return res


@event_place_router_v1.patch("/{id}", response=EventPlaceSchema)
def update(request, id: int, data: EventPlaceUpdateSchema):
    _require_superuser(request)
    item = get_object_or_404(EventPlace, pk=id)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(item, attr, value)
    item.save()
    return item


@event_place_router_v1.delete("/{id}", response={204: None})
def delete(request, id: int):
    _require_superuser(request)
    item = get_object_or_404(EventPlace, pk=id)
    item.delete()
    return
