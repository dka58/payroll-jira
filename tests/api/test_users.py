from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.utils.security import create_access_token
from app.core.config import settings
from app.models.user import UserCreate
from app.api.dependencies.users import get_user_by_email
from app.api.routes.users import router
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_in.dict()
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert "id" in content
    assert "hashed_password" not in content

    user_db = get_user_by_email(db, email=email)
    assert user_db is not None
    assert user_db.email == email
    assert user_db.is_active


def test_create_user_existing_email(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_in.dict()
    )
    assert response.status_code == 200

    # repeat with same email
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_in.dict()
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "The user with this email already exists in the system."


def test_retrieve_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_in.dict()
    )
    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/users/{email}"
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert "id" in content
    assert "hashed_password" not in content


def test_retrieve_user_wrong_email(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_in.dict()
    )
    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/users/{random_email()}"
    )
    assert response.status_code == 404


def test_update_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=user_in.dict()
    )
    assert response.status_code == 200

    access_token = create_access_token(data={"sub": email})
    new_password = random_lower_string()
    data = {"password": new_password}
    response = client.put(
        f"{settings.API_V1_STR}/users/me", json=data, headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    user_db = get_user_by_email(db, email=email)
    assert user_db is not None
    assert user_db.email == email

    # Check that password has been updated
    updated_user = response.json()
    assert updated_user["email"] == email
    assert "id" in updated_user
    assert "hashed_password" not in updated_user

    # Check that new password is correct
    access_token = create_access_token(data={"sub": email})
    response = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={"username": email, "password": new_password},
    )
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"

