from ninja import NinjaAPI
from ninja_jwt.routers.obtain import obtain_pair_router
from ninja_jwt.routers.verify import verify_router

from app_event.api import event_router_v1
from app_event_place.api import event_place_router_v1

api = NinjaAPI()

api.add_router("/v1/event_place", event_place_router_v1)
api.add_router("/v1/event", event_router_v1)
api.add_router("/v1/auth/token", obtain_pair_router)
api.add_router("/v1/auth/token", verify_router)


@api.get("/heathcheck")
def hello(request):
    return "OK"
