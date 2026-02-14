from ninja import NinjaAPI

from app_event_place.api import event_place_router_v1

api = NinjaAPI()

api.add_router("/v1/event_place", event_place_router_v1)


@api.get("/heathcheck")
def hello(request):
    return "OK"
