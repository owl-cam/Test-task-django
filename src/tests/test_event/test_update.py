from unittest.mock import patch


def test_update_superuser(client, superuser_headers, published_event):
    response = client.patch(
        f"/v1/event/{published_event.id}",
        json={"name": "Updated Event"},
        headers=superuser_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Event"

    published_event.refresh_from_db()
    assert published_event.name == "Updated Event"


def test_update_partial(client, superuser_headers, published_event):
    original_rate = published_event.rate
    response = client.patch(
        f"/v1/event/{published_event.id}",
        json={"name": "Partial Update"},
        headers=superuser_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Partial Update"
    assert data["rate"] == original_rate


def test_update_signal_on_false_to_true(client, superuser_headers, unpublished_event):
    with patch("post_office.mail.send") as mock_send:
        response = client.patch(
            f"/v1/event/{unpublished_event.id}",
            json={"published": True},
            headers=superuser_headers,
        )
    assert response.status_code == 200
    mock_send.assert_called_once()


def test_update_no_signal_when_already_published(client, superuser_headers, published_event):
    with patch("post_office.mail.send") as mock_send:
        response = client.patch(
            f"/v1/event/{published_event.id}",
            json={"name": "Still Published"},
            headers=superuser_headers,
        )
    assert response.status_code == 200
    mock_send.assert_not_called()


def test_update_nonexistent_returns_404(client, superuser_headers, db):
    response = client.patch(
        "/v1/event/99999",
        json={"name": "Ghost"},
        headers=superuser_headers,
    )
    assert response.status_code == 404


def test_update_regular_user_forbidden(client, regular_user_headers, published_event):
    response = client.patch(
        f"/v1/event/{published_event.id}",
        json={"name": "Hack"},
        headers=regular_user_headers,
    )
    assert response.status_code == 403


def test_update_unauthenticated(client, published_event):
    response = client.patch(
        f"/v1/event/{published_event.id}",
        json={"name": "Hack"},
    )
    assert response.status_code == 401
