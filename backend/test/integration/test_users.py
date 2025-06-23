import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.security.jwt import create_access_token 
from datetime import timedelta
from fastapi import status
from app.services.user_service import create_user as service_create_user
from app.schemas.user import UserCreate

TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"
TEST_USER_NAME = "Test User"

def create_test_user_in_db(db: Session):
    user_data = UserCreate(nome=TEST_USER_NAME, email=TEST_USER_EMAIL, senha=TEST_USER_PASSWORD)
    return service_create_user(user_data, db)

def get_auth_headers(user_id: int): 
    access_token = create_access_token(data={"user_id": user_id})
    return {"Authorization": f"Bearer {access_token}"}

def test_create_user_success(client_with_db: TestClient):

    user_data = {
        "nome": "New User",
        "email": "newuser@example.com",
        "senha": "securepassword123"
    }
    response = client_with_db.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["nome"] == user_data["nome"]
    assert "id" in data
    assert "senha_hash" not in data 

def test_create_user_duplicate_email(client_with_db: TestClient, db_session: Session):

    create_test_user_in_db(db_session)

    duplicate_user_data = {
        "nome": "Another User",
        "email": TEST_USER_EMAIL,
        "senha": "anotherpassword"
    }
    response = client_with_db.post("/api/v1/users/", json=duplicate_user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Um usuário com este e-mail já existe."

def test_create_user_invalid_input(client_with_db: TestClient):
    invalid_user_data = {
        "nome": "Invalid User",
        "senha": "password123"
    }
    response = client_with_db.post("/api/v1/users/", json=invalid_user_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_read_users_me_success(client_with_db: TestClient, db_session: Session):

    user = create_test_user_in_db(db_session)
    headers = get_auth_headers(user.id)

    response = client_with_db.get("/api/v1/users/me/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user.email
    assert data["nome"] == user.nome
    assert "id" in data
    assert "senha_hash" not in data

def test_read_users_me_unauthorized_no_token(client_with_db: TestClient):
    response = client_with_db.get("/api/v1/users/me/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"

def test_read_users_me_invalid_token(client_with_db: TestClient):

    headers = {"Authorization": "Bearer some.invalid.token"}
    response = client_with_db.get("/api/v1/users/me/", headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"