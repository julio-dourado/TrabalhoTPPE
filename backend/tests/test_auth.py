import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Testa registro de novo usuário"""
    user_data = {
        "nome": "New User",
        "email": "newuser@example.com",
        "password": "newpass123"
    }
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["nome"] == user_data["nome"]
    assert "id" in data


def test_register_duplicate_email(client: TestClient, test_user):
    """Testa erro ao registrar email duplicado"""
    user_data = {
        "nome": "Duplicate User",
        "email": test_user.email,
        "password": "pass123"
    }
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == 400
    assert "já está registrado" in response.json()["detail"]


def test_login_success(client: TestClient, test_user):
    """Testa login com credenciais válidas"""
    login_data = {
        "username": test_user.email,
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, test_user):
    """Testa login com credenciais inválidas"""
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "incorretos" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient):
    """Testa login com usuário inexistente"""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password123"
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 401


def test_get_current_user(client: TestClient, auth_headers):
    """Testa endpoint para obter usuário atual"""
    response = client.get("/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "nome" in data


def test_get_current_user_without_token(client: TestClient):
    """Testa acesso sem token de autenticação"""
    response = client.get("/auth/me")
    
    assert response.status_code == 401 