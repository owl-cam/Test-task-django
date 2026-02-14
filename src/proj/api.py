from ninja import NinjaAPI

api = NinjaAPI(version="1")


@api.get("/heathcheck")
def hello(request):
    return "OK"
