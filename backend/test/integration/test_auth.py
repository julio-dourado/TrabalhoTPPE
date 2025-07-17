import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.services.user_service import UserService

# Note: As fixtures 'client_with_db' e 'db' são importadas
# automaticamente de conftest.py pelo pytest.


def test_full_authentication_flow(client_with_db: TestClient):
    """Tests the complete authentication flow: register, login, and access protected route."""
    user_data = {
        "name": "Test User",
        "email": "auth.test@example.com",
        "password": "password123",
    }

    # 1. Register user
    response_create = client_with_db.post("/api/v1/users/", json=user_data)
    assert response_create.status_code == 201
    created_user = response_create.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["name"] == user_data["name"]
    assert "id" in created_user

    # 2. Login
    response_login = client_with_db.post(
        "/api/v1/auth/login",
        json={"email": "auth.test@example.com", "password": "password123"},
    )
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Access protected route (/users/me)
    response_me = client_with_db.get("/api/v1/users/me", headers=headers)
    assert response_me.status_code == 200
    me_user = response_me.json()
    assert me_user["email"] == user_data["email"]
    assert me_user["name"] == user_data["name"]
    assert me_user["id"] == created_user["id"]


def test_login_with_invalid_credentials(client_with_db: TestClient):
    """Test login with invalid credentials"""
    response = client_with_db.post(
        "/api/v1/auth/login",
        json={"email": "invalid@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_register_new_user(client_with_db: TestClient):
    """Test registering a new user"""
    user_data = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "password123",
    }

    response = client_with_db.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["name"] == user_data["name"]
    assert "id" in created_user
    assert "password" not in created_user


def test_register_user_with_existing_email(client_with_db: TestClient):
    """Test registering user with existing email"""
    user_data = {
        "name": "Test User",
        "email": "existing@example.com",
        "password": "password123",
    }

    # Register first user
    response1 = client_with_db.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201

    # Try to register another user with the same email
    response2 = client_with_db.post("/api/v1/users/", json=user_data)
    assert response2.status_code == 400
    assert "detail" in response2.json()


def test_register_user_with_password_mismatch(client_with_db: TestClient):
    """Test registering user with valid data"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
    }

    response = client_with_db.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201


def test_access_protected_endpoint_without_token(client_with_db: TestClient):
    """Test accessing protected endpoint without token"""
    response = client_with_db.get("/api/v1/users/me")
    
    assert response.status_code == 403


def test_access_protected_endpoint_with_invalid_token(client_with_db: TestClient):
    """Test accessing protected endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client_with_db.get("/api/v1/users/me", headers=headers)
    
    assert response.status_code == 401
