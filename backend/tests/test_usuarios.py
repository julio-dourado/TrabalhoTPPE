import pytest
from fastapi.testclient import TestClient


def test_read_usuarios(client: TestClient, auth_headers, test_user):
    """Testa listagem de usuários"""
    response = client.get("/usuarios/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_my_profile(client: TestClient, auth_headers, test_user):
    """Testa obtenção do perfil do usuário atual"""
    response = client.get("/usuarios/me/profile", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["nome"] == test_user.nome
    assert data["is_active"] == True
    
    # Testar perfil completo
    response_complete = client.get("/usuarios/me/profile-complete", headers=auth_headers)
    assert response_complete.status_code == 200
    data_complete = response_complete.json()
    assert "treinos" in data_complete


def test_read_usuario_by_id(client: TestClient, auth_headers, test_user):
    """Testa busca de usuário por ID"""
    response = client.get(f"/usuarios/{test_user.id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


def test_read_nonexistent_usuario(client: TestClient, auth_headers):
    """Testa busca de usuário inexistente"""
    response = client.get("/usuarios/99999", headers=auth_headers)
    
    assert response.status_code == 404


def test_update_my_profile(client: TestClient, auth_headers, test_user):
    """Testa atualização do perfil do usuário atual"""
    update_data = {
        "nome": "Updated Name"
    }
    response = client.put("/usuarios/me", headers=auth_headers, json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Updated Name"
    assert data["email"] == test_user.email


def test_update_my_profile_with_email(client: TestClient, auth_headers):
    """Testa atualização do email do usuário"""
    update_data = {
        "email": "newemail@example.com",
        "nome": "Test User Updated"
    }
    response = client.put("/usuarios/me", headers=auth_headers, json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newemail@example.com"


def test_delete_my_account(client: TestClient, auth_headers):
    """Testa exclusão da própria conta"""
    response = client.delete("/usuarios/me", headers=auth_headers)
    
    assert response.status_code == 204


def test_access_without_auth(client: TestClient):
    """Testa acesso aos endpoints de usuário sem autenticação"""
    response = client.get("/usuarios/")
    
    assert response.status_code == 401 