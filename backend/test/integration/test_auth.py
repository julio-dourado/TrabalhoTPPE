import pytest
from fastapi.testclient import TestClient


def test_full_authentication_flow(client_with_db: TestClient):
    user_data = {
        "nome": "Usuário de Teste Auth",
        "email": "auth.test@exemplo.com",
        "senha": "senha_super_segura_123"
    }
    # Ajustado para /api/v1/users/
    response_create = client_with_db.post("/api/v1/users/", json=user_data)
    assert response_create.status_code == 201, "Falha ao criar usuário para o teste de login"
    created_user = response_create.json()
    
    login_data = {
        "username": user_data["email"],
        "password": user_data["senha"]
    }
    response_login = client_with_db.post("/api/v1/auth/token", data=login_data)
    
    assert response_login.status_code == 200, "O login falhou com credenciais corretas"
    token_info = response_login.json()
    access_token = token_info["access_token"]
    
    headers = {"Authorization": f"Bearer {access_token}"}

    response_me = client_with_db.get("/api/v1/users/me/", headers=headers)
    
    assert response_me.status_code == 200, "Falha ao acessar a rota protegida com um token válido"
    profile_data = response_me.json()
    assert profile_data["email"] == user_data["email"]
    assert profile_data["id"] == created_user["id"]

def test_login_with_wrong_password_fails(client_with_db: TestClient):

    user_data = { "nome": "Usuário Senha Errada", "email": "wrong.password@exemplo.com", "senha": "senha_correta" }
    client_with_db.post("/api/v1/users/", json=user_data)
    
    login_data = { "username": user_data["email"], "password": "senha_errada_propositalmente" }
    response_login = client_with_db.post("/api/v1/auth/token", data=login_data)
    
    assert response_login.status_code == 401

def test_access_protected_route_without_token_fails(client_with_db: TestClient):

    response = client_with_db.get("/api/v1/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


    headers = {"Authorization": "Bearer token_falso_e_invalido"}
    response = client_with_db.get("/api/v1/users/me/", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
