from app_event.models import Event


def test_delete_superuser(client, superuser_headers, published_event):
    event_id = published_event.id
    response = client.delete(f"/v1/event/{event_id}", headers=superuser_headers)
    assert response.status_code == 204
    assert not Event.objects.filter(pk=event_id).exists()


def test_delete_nonexistent_returns_404(client, superuser_headers, db):
    response = client.delete("/v1/event/99999", headers=superuser_headers)
    assert response.status_code == 404


def test_delete_regular_user_forbidden(client, regular_user_headers, published_event):
    response = client.delete(
        f"/v1/event/{published_event.id}", headers=regular_user_headers
    )
    assert response.status_code == 403


def test_delete_unauthenticated(client, published_event):
    response = client.delete(f"/v1/event/{published_event.id}")
    assert response.status_code == 401
