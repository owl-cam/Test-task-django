def test_get_published_regular_user(client, regular_user_headers, published_event):
    response = client.get(
        f"/v1/event/{published_event.id}", headers=regular_user_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == published_event.id


def test_get_unpublished_regular_user_returns_404(
    client, regular_user_headers, unpublished_event
):
    response = client.get(
        f"/v1/event/{unpublished_event.id}", headers=regular_user_headers
    )
    assert response.status_code == 404


def test_get_superuser(client, superuser_headers, published_event):
    response = client.get(
        f"/v1/event/{published_event.id}", headers=superuser_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == published_event.id


def test_get_nonexistent_returns_404(client, superuser_headers, db):
    response = client.get("/v1/event/99999", headers=superuser_headers)
    assert response.status_code == 404


def test_get_unauthenticated(client, published_event):
    response = client.get(f"/v1/event/{published_event.id}")
    assert response.status_code == 401
