def test_update_superuser(client, superuser_headers, event_place):
    response = client.patch(
        f"/v1/event_place/{event_place.id}",
        json={"name": "Updated Venue"},
        headers=superuser_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Venue"

    event_place.refresh_from_db()
    assert event_place.name == "Updated Venue"


def test_update_partial(client, superuser_headers, event_place):
    original_lat = event_place.lat
    response = client.patch(
        f"/v1/event_place/{event_place.id}",
        json={"name": "Partial Update"},
        headers=superuser_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Partial Update"
    assert data["lat"] == original_lat


def test_update_nonexistent_returns_404(client, superuser_headers, db):
    response = client.patch(
        "/v1/event_place/99999",
        json={"name": "Ghost Venue"},
        headers=superuser_headers,
    )
    assert response.status_code == 404


def test_update_regular_user_forbidden(client, regular_user_headers, event_place):
    response = client.patch(
        f"/v1/event_place/{event_place.id}",
        json={"name": "Hack"},
        headers=regular_user_headers,
    )
    assert response.status_code == 403


def test_update_unauthenticated(client, event_place):
    response = client.patch(
        f"/v1/event_place/{event_place.id}",
        json={"name": "Hack"},
    )
    assert response.status_code == 401
