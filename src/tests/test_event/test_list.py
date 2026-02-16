from app_event.models import Event


def test_list_regular_user_only_published(client, regular_user_headers, published_event, unpublished_event):
    response = client.get("/v1/event", headers=regular_user_headers)
    assert response.status_code == 200
    data = response.json()
    ids = [e["id"] for e in data["data"]]
    assert published_event.id in ids
    assert unpublished_event.id not in ids


def test_list_superuser_sees_all(client, superuser_headers, published_event, unpublished_event):
    response = client.get("/v1/event", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    ids = [e["id"] for e in data["data"]]
    assert published_event.id in ids
    assert unpublished_event.id in ids


def test_list_pagination(client, regular_user_headers, event_place, db):
    for i in range(5):
        Event.objects.create(
            published=True,
            name=f"Event {i}",
            description="desc",
            start_date="2025-06-01T10:00:00Z",
            end_date="2025-06-01T18:00:00Z",
            author="Author",
            place=event_place,
            rate=1,
            status=Event.SOON,
        )

    response = client.get("/v1/event?limit=2&offset=0", headers=regular_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["total"] == 5


def test_list_filter_published(client, superuser_headers, published_event, unpublished_event):
    response = client.get("/v1/event?published=true", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    ids = [e["id"] for e in data["data"]]
    assert published_event.id in ids
    assert unpublished_event.id not in ids


def test_list_filter_rate_gte(client, regular_user_headers, db):
    Event.objects.create(
        published=True,
        name="High Rate",
        description="desc",
        start_date="2025-06-01T10:00:00Z",
        end_date="2025-06-01T18:00:00Z",
        author="Author",
        rate=20,
        status=Event.SOON,
    )
    Event.objects.create(
        published=True,
        name="Low Rate",
        description="desc",
        start_date="2025-06-01T10:00:00Z",
        end_date="2025-06-01T18:00:00Z",
        author="Author",
        rate=1,
        status=Event.SOON,
    )

    response = client.get("/v1/event?rate_gte=15", headers=regular_user_headers)
    assert response.status_code == 200
    data = response.json()
    names = [e["name"] for e in data["data"]]
    assert "High Rate" in names
    assert "Low Rate" not in names


def test_list_filter_query(client, regular_user_headers, published_event, db):
    response = client.get(f"/v1/event?query={published_event.name[:5]}", headers=regular_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert any(e["id"] == published_event.id for e in data["data"])


def test_list_filter_place_id_in(client, superuser_headers, published_event, event_place):
    response = client.get(f"/v1/event?place_id_in={event_place.id}", headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert any(e["id"] == published_event.id for e in data["data"])


def test_list_unauthenticated(client):
    response = client.get("/v1/event")
    assert response.status_code == 401
