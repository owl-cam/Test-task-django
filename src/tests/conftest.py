import pytest
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken

from app_event.models import Event
from app_event_place.models import EventPlace
from proj.api import api


@pytest.fixture(scope="session")
def client():
    return TestClient(api)


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        username="admin", password="adminpass123", email="admin@example.com"
    )


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        username="user", password="userpass123", email="user@example.com"
    )


def _auth_headers(user):
    refresh = RefreshToken.for_user(user)
    return {"Authorization": f"Bearer {refresh.access_token}"}


@pytest.fixture
def superuser_headers(superuser):
    return _auth_headers(superuser)


@pytest.fixture
def regular_user_headers(regular_user):
    return _auth_headers(regular_user)


@pytest.fixture
def event_place(db):
    return EventPlace.objects.create(
        name="Test Venue",
        lat=55.7558,
        long=37.6173,
    )


@pytest.fixture
def published_event(db, event_place):
    return Event.objects.create(
        published=True,
        name="Published Event",
        description="A published event",
        start_date="2025-06-01T10:00:00Z",
        end_date="2025-06-01T18:00:00Z",
        author="Test Author",
        place=event_place,
        rate=10,
        status=Event.SOON,
    )


@pytest.fixture
def unpublished_event(db, event_place):
    return Event.objects.create(
        published=False,
        name="Unpublished Event",
        description="An unpublished event",
        start_date="2025-07-01T10:00:00Z",
        end_date="2025-07-01T18:00:00Z",
        author="Test Author",
        place=event_place,
        rate=5,
        status=Event.SOON,
    )
