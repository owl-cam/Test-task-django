from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from app_event_place.domain import EventPlaceDomain
from app_weather.domain import WeatherDomain

from .domain import (
    EventCreateDomain,
    EventDomain,
    EventFilterDomain,
    EventListDomain,
    EventOrder,
    EventUpdateDomain,
)
from .models import Event


class EventService:
    def get_by_id(self, current_user, item_id: int) -> EventDomain:
        filters = EventFilterDomain(id=item_id)
        if not getattr(current_user, "is_superuser", False):
            filters.published = True
        return self._get_one(filters)

    def get_list(
        self,
        current_user,
        limit: int,
        offset: int,
        filters: EventFilterDomain,
        order: EventOrder | None = None,
    ) -> EventListDomain:
        if not getattr(current_user, "is_superuser", False):
            filters.published = True
        total = self._count(filters)
        if total == 0:
            return EventListDomain(data=[], total=0, limit=limit, offset=offset)
        filters_list, filters_dict = self._prepare_filters(filters)
        data = Event.objects.select_related("place", "place__weather").filter(
            *filters_list, **filters_dict
        )
        if order:
            data = data.order_by(order.value)
        data = data[offset : limit + offset]
        data = [self._to_domain(_) for _ in data]
        return EventListDomain(data=data, total=total, limit=limit, offset=offset)

    def create(self, data: EventCreateDomain) -> EventDomain:
        db_model = Event(**data.model_dump())
        db_model.save()
        return self._get_one(EventFilterDomain(id=db_model.pk))

    def update(self, item_id: int, data: EventUpdateDomain) -> EventDomain:
        db_model = get_object_or_404(Event, pk=item_id)
        for attr, value in data.model_dump(exclude_unset=True).items():
            setattr(db_model, attr, value)
        db_model.save()
        return self._get_one(EventFilterDomain(id=item_id))

    def delete(self, item_id: int) -> None:
        db_model = get_object_or_404(Event, pk=item_id)
        db_model.delete()

    def _get_one(self, filters: EventFilterDomain) -> EventDomain:
        filters_list, filters_dict = self._prepare_filters(filters)
        db_model = (
            Event.objects.select_related("place", "place__weather")
            .filter(*filters_list, **filters_dict)
            .first()
        )
        if not db_model:
            raise Http404
        return self._to_domain(db_model)

    def _count(self, filters: EventFilterDomain) -> int:
        filters_list, filters_dict = self._prepare_filters(filters)
        return Event.objects.filter(*filters_list, **filters_dict).count()

    def _prepare_filters(self, filters: EventFilterDomain):
        filters_list, filters_dict = [], {}
        if filters:
            if filters.id is not None:
                filters_dict["id"] = filters.id
            if filters.published is not None:
                filters_dict["published"] = filters.published
            if filters.start_date_gte is not None:
                filters_dict["start_date__gte"] = filters.start_date_gte
            if filters.start_date_lte is not None:
                filters_dict["start_date__lte"] = filters.start_date_lte
            if filters.end_date_gte is not None:
                filters_dict["end_date__gte"] = filters.end_date_gte
            if filters.end_date_lte is not None:
                filters_dict["end_date__lte"] = filters.end_date_lte
            if filters.place_id_in is not None:
                filters_dict["place_id__in"] = filters.place_id_in
            if filters.rate_gte is not None:
                filters_dict["rate__gte"] = filters.rate_gte
            if filters.rate_lte is not None:
                filters_dict["rate__lte"] = filters.rate_lte
            if filters.query is not None:
                filters_list.append(
                    Q(name__icontains=filters.query)
                    | Q(place__name__icontains=filters.query)
                )
        return filters_list, filters_dict

    def _to_domain(self, event: Event) -> EventDomain:
        place = None
        if event.place_id is not None:
            weather = None
            try:
                w = event.place.weather
                weather = WeatherDomain(
                    temp=w.temp,
                    condition=w.condition,
                    humidity=w.humidity,
                    pressure=w.pressure,
                    wind_dir=w.wind_dir,
                    wind_speed=w.wind_speed,
                )
            except Exception:
                pass
            place = EventPlaceDomain(
                id=event.place.id,
                name=event.place.name,
                long=event.place.long,
                lat=event.place.lat,
                weather=weather,
            )
        return EventDomain(
            id=event.id,
            published=event.published,
            name=event.name,
            description=event.description,
            publish_date=event.publish_date,
            start_date=event.start_date,
            end_date=event.end_date,
            author=event.author,
            place_id=event.place_id,
            place=place,
            rate=event.rate,
            status=event.status,
        )
