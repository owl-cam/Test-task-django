from django.http import HttpResponse
from ninja import File, Query, Router
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth

from app_event.domain import EventOrder
from app_event.service import EventService
from app_event.xlsx import EventXlsxService

from .schema import (
    EventCreateSchema,
    EventExportFilterSchema,
    EventFilterSchema,
    EventImageSchema,
    EventListSchema,
    EventSchema,
    EventUpdateSchema,
    ImportResultSchema,
)

event_router_v1 = Router(tags=["event"], auth=JWTAuth())

service = EventService()
xlsx_service = EventXlsxService()


@event_router_v1.get("/export")
def export_xlsx(request, filters: Query[EventExportFilterSchema]):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")

    filters_dict = filters.dict(exclude_none=True)
    xlsx_data = xlsx_service.export_events(filters_dict)

    response = HttpResponse(
        xlsx_data.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="events.xlsx"'
    return response


@event_router_v1.post("/import", response=ImportResultSchema)
def import_xlsx(request, file: File[UploadedFile]):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")

    file_data = file.read()
    result = xlsx_service.import_events(file_data, author=request.user.username)
    return result


@event_router_v1.post("/image", response=EventImageSchema)
def upload_image(request, event_id: int, image: File[UploadedFile]):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")
    return service.upload_image(image, event_id)


@event_router_v1.delete("/image/{id}", response={204: None})
def delete_image(request, id: int):
    if not request.user.is_superuser:
        raise HttpError(403, "Forbidden")
    return service.remove_image(id)


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
