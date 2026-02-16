def test_get_by_id_superuser(client, superuser_headers, event_place):
    response = client.get(f"/v1/event_place/{event_place.id}", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_place.id
    assert data["name"] == event_place.name


def test_get_by_id_nonexistent_returns_404(client, superuser_headers, db):
    response = client.get("/v1/event_place/99999", headers=superuser_headers)
    assert response.status_code == 404


def test_get_by_id_regular_user_forbidden(client, regular_user_headers, event_place):
    response = client.get(f"/v1/event_place/{event_place.id}", headers=regular_user_headers)
    assert response.status_code == 403


def test_get_by_id_unauthenticated(client, event_place):
    response = client.get(f"/v1/event_place/{event_place.id}")
    assert response.status_code == 401
