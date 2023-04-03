from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.api.utils.auth import create_access_token
from app.config import JWT_TOKEN_PREFIX
from app.main import app


def test_create_access_token():
    email = "test@example.com"
    access_token = create_access_token(email)
    assert access_token.startswith(JWT_TOKEN_PREFIX)


def test_create_jwt_token(test_app: TestClient, test_db: Session):
    response = test_app.post(
        "/api/auth/token",
        data={"email": "test@example.com", "password": "password"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_refresh_jwt_token(test_app: TestClient, test_db: Session):
    response = test_app.post(
        "/api/auth/token/refresh",
        headers={"Authorization": f"Bearer {create_access_token('test@example.com')}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_register_user(test_app: TestClient, test_db: Session):
    response = test_app.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password",
            "full_name": "Test User",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "test@example.com"
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_user(test_app: TestClient, test_db: Session):
    response = test_app.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "password"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
