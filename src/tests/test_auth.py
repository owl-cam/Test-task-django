import pytest


@pytest.fixture
def user_with_credentials(db):
    from django.contrib.auth.models import User
    user = User.objects.create_user(username="authuser", password="authpass123")
    return user


def test_token_pair_success(client, user_with_credentials):
    response = client.post(
        "/v1/auth/token/pair",
        json={"username": "authuser", "password": "authpass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "refresh" in data


def test_token_pair_wrong_password(client, user_with_credentials):
    response = client.post(
        "/v1/auth/token/pair",
        json={"username": "authuser", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_token_pair_nonexistent_user(client, db):
    response = client.post(
        "/v1/auth/token/pair",
        json={"username": "nobody", "password": "pass"},
    )
    assert response.status_code == 401


def test_token_pair_missing_fields(client, db):
    # ninja-jwt returns 400 (not 422) for missing required fields
    response = client.post("/v1/auth/token/pair", json={})
    assert response.status_code == 400


def test_token_verify_valid(client, user_with_credentials):
    pair_response = client.post(
        "/v1/auth/token/pair",
        json={"username": "authuser", "password": "authpass123"},
    )
    access = pair_response.json()["access"]

    response = client.post("/v1/auth/token/verify", json={"token": access})
    assert response.status_code == 200


def test_token_verify_invalid(client, db):
    response = client.post("/v1/auth/token/verify", json={"token": "invalid.token.here"})
    assert response.status_code == 401


def test_token_refresh_valid(client, user_with_credentials):
    pair_response = client.post(
        "/v1/auth/token/pair",
        json={"username": "authuser", "password": "authpass123"},
    )
    refresh = pair_response.json()["refresh"]

    response = client.post("/v1/auth/token/refresh", json={"refresh": refresh})
    assert response.status_code == 200
    assert "access" in response.json()


def test_token_refresh_invalid(client, db):
    response = client.post("/v1/auth/token/refresh", json={"refresh": "invalid.token"})
    assert response.status_code == 401
