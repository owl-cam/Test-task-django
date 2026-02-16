from app_event_place.models import EventPlace


def test_create_superuser(client, superuser_headers, db):
    payload = {"name": "New Venue", "lat": 55.0, "long": 37.0}
    response = client.post("/v1/event_place", json=payload, headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Venue"
    assert EventPlace.objects.filter(name="New Venue").exists()


def test_create_regular_user_forbidden(client, regular_user_headers):
    payload = {"name": "New Venue", "lat": 55.0, "long": 37.0}
    response = client.post("/v1/event_place", json=payload, headers=regular_user_headers)
    assert response.status_code == 403


def test_create_unauthenticated(client):
    payload = {"name": "New Venue", "lat": 55.0, "long": 37.0}
    response = client.post("/v1/event_place", json=payload)
    assert response.status_code == 401


def test_create_invalid_data(client, superuser_headers, db):
    # Missing required fields
    response = client.post("/v1/event_place", json={}, headers=superuser_headers)
    assert response.status_code == 422
