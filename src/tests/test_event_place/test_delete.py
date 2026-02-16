from app_event_place.models import EventPlace


def test_delete_superuser(client, superuser_headers, event_place):
    place_id = event_place.id
    response = client.delete(f"/v1/event_place/{place_id}", headers=superuser_headers)
    assert response.status_code == 204
    assert not EventPlace.objects.filter(pk=place_id).exists()


def test_delete_nonexistent_returns_404(client, superuser_headers, db):
    response = client.delete("/v1/event_place/99999", headers=superuser_headers)
    assert response.status_code == 404


def test_delete_regular_user_forbidden(client, regular_user_headers, event_place):
    response = client.delete(f"/v1/event_place/{event_place.id}", headers=regular_user_headers)
    assert response.status_code == 403


def test_delete_unauthenticated(client, event_place):
    response = client.delete(f"/v1/event_place/{event_place.id}")
    assert response.status_code == 401
