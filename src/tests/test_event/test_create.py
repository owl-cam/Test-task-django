from unittest.mock import patch

from app_event.models import Event


EVENT_PAYLOAD = {
    "published": False,
    "name": "New Event",
    "description": "A new event",
    "start_date": "2025-08-01T10:00:00Z",
    "end_date": "2025-08-01T18:00:00Z",
    "author": "Author",
    "rate": 5,
    "status": "soon",
}


def test_create_superuser(client, superuser_headers, db):
    response = client.post("/v1/event", json=EVENT_PAYLOAD, headers=superuser_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Event"
    assert Event.objects.filter(name="New Event").exists()


def test_create_no_signal_when_unpublished(client, superuser_headers, db):
    payload = {**EVENT_PAYLOAD, "published": False}
    with patch("post_office.mail.send") as mock_send:
        response = client.post("/v1/event", json=payload, headers=superuser_headers)
    assert response.status_code == 200
    mock_send.assert_not_called()


def test_create_signal_when_published(client, superuser_headers, db):
    payload = {**EVENT_PAYLOAD, "published": True}
    with patch("post_office.mail.send") as mock_send:
        response = client.post("/v1/event", json=payload, headers=superuser_headers)
    assert response.status_code == 200
    mock_send.assert_called_once()


def test_create_regular_user_forbidden(client, regular_user_headers, db):
    response = client.post("/v1/event", json=EVENT_PAYLOAD, headers=regular_user_headers)
    assert response.status_code == 403


def test_create_unauthenticated(client, db):
    response = client.post("/v1/event", json=EVENT_PAYLOAD)
    assert response.status_code == 401


def test_create_missing_name(client, superuser_headers, db):
    payload = {k: v for k, v in EVENT_PAYLOAD.items() if k != "name"}
    response = client.post("/v1/event", json=payload, headers=superuser_headers)
    assert response.status_code == 422
