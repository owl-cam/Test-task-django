from app_event_place.models import EventPlace


def test_list_superuser(client, superuser_headers, event_place):
    response = client.get("/v1/event_place", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert data["total"] >= 1


def test_list_pagination(client, superuser_headers, db):
    for i in range(5):
        EventPlace.objects.create(name=f"Venue {i}", lat=0, long=0)

    response = client.get("/v1/event_place?limit=2&offset=0", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 0
    assert data["total"] == 5


def test_list_pagination_offset(client, superuser_headers, db):
    for i in range(5):
        EventPlace.objects.create(name=f"Venue {i}", lat=0, long=0)

    response = client.get("/v1/event_place?limit=2&offset=3", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2


def test_list_regular_user_forbidden(client, regular_user_headers):
    response = client.get("/v1/event_place", headers=regular_user_headers)
    assert response.status_code == 403


def test_list_unauthenticated(client):
    response = client.get("/v1/event_place")
    assert response.status_code == 401
