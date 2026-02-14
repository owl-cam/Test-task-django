from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import django_auth_superuser

from app_event_place.models import EventPlace

from .schema import (
    EventPlaceCreateSchema,
    EventPlaceListSchema,
    EventPlaceSchema,
    EventPlaceUpdateSchema,
)

event_place_router_v1 = Router(tags=["event_place"])


@event_place_router_v1.get(
    "/{id}", response=EventPlaceSchema, auth=django_auth_superuser
)
def get_by_id(request, id: int):
    return EventPlace.objects.filter(pk=id).first()


@event_place_router_v1.get(
    "", response=EventPlaceListSchema, auth=django_auth_superuser
)
def get_all(
    request,
    offset: int = 0,
    limit: int = 20,
):
    return EventPlaceListSchema(
        data=EventPlace.objects.all()[offset : limit + offset],
        total=EventPlace.objects.count(),
    )


@event_place_router_v1.post("", response=EventPlaceSchema, auth=django_auth_superuser)
def create(request, data: EventPlaceCreateSchema):
    res = EventPlace(**data.dict())
    res.save()
    return res


@event_place_router_v1.patch(
    "/{id}", response=EventPlaceSchema, auth=django_auth_superuser
)
def update(request, id: int, data: EventPlaceUpdateSchema):
    item = get_object_or_404(EventPlace, pk=id)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(item, attr, value)
    item.save()
    return item


@event_place_router_v1.delete("/{id}", response={204: None}, auth=django_auth_superuser)
def delete(request, id: int):
    item = get_object_or_404(EventPlace, pk=id)
    item.delete()
    return
