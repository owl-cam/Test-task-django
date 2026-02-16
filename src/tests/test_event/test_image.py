from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import pytest

from app_event.models import EventImage


def _create_test_image():
    """Create minimal PNG for tests."""
    img = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


@pytest.fixture
def event_image(db, published_event):
    """Create an EventImage for tests."""
    image = EventImage(event=published_event)
    image.image.save("test.png", ContentFile(_create_test_image()))
    return image


# Upload image tests


def test_upload_image_superuser(client, superuser_headers, published_event, db):
    image_file = SimpleUploadedFile(
        "test.png",
        _create_test_image(),
        content_type="image/png",
    )

    response = client.post(
        f"/v1/event/image?event_id={published_event.id}",
        headers=superuser_headers,
        FILES={"image": image_file},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "image" in data
    assert "image_thumbnail" in data
    assert EventImage.objects.filter(event=published_event).exists()


def test_upload_image_regular_user_forbidden(
    client, regular_user_headers, published_event, db
):
    image_file = SimpleUploadedFile(
        "test.png",
        _create_test_image(),
        content_type="image/png",
    )

    response = client.post(
        f"/v1/event/image?event_id={published_event.id}",
        headers=regular_user_headers,
        FILES={"image": image_file},
    )
    assert response.status_code == 403


def test_upload_image_unauthenticated(client, published_event, db):
    image_file = SimpleUploadedFile(
        "test.png",
        _create_test_image(),
        content_type="image/png",
    )

    response = client.post(
        f"/v1/event/image?event_id={published_event.id}",
        FILES={"image": image_file},
    )
    assert response.status_code == 401


def test_upload_image_event_not_found(client, superuser_headers, db):
    image_file = SimpleUploadedFile(
        "test.png",
        _create_test_image(),
        content_type="image/png",
    )

    response = client.post(
        "/v1/event/image?event_id=99999",
        headers=superuser_headers,
        FILES={"image": image_file},
    )
    assert response.status_code == 404


# Delete image tests


def test_delete_image_superuser(client, superuser_headers, event_image, db):
    image_id = event_image.id

    response = client.delete(
        f"/v1/event/image/{image_id}",
        headers=superuser_headers,
    )
    assert response.status_code == 204
    assert not EventImage.objects.filter(id=image_id).exists()


def test_delete_image_not_found(client, superuser_headers, db):
    response = client.delete(
        "/v1/event/image/99999",
        headers=superuser_headers,
    )
    assert response.status_code == 404


def test_delete_image_regular_user_forbidden(
    client, regular_user_headers, event_image, db
):
    response = client.delete(
        f"/v1/event/image/{event_image.id}",
        headers=regular_user_headers,
    )
    assert response.status_code == 403
    assert EventImage.objects.filter(id=event_image.id).exists()


def test_delete_image_unauthenticated(client, event_image, db):
    response = client.delete(
        f"/v1/event/image/{event_image.id}",
    )
    assert response.status_code == 401
    assert EventImage.objects.filter(id=event_image.id).exists()
