import pytest
from fastapi.testclient import TestClient


def test_create_treino(client: TestClient, auth_headers):
    """Testa criação de novo treino"""
    treino_data = {
        "nome": "Treino de Teste",
        "descricao": "Descrição do treino de teste"
    }
    response = client.post("/treinos/", headers=auth_headers, json=treino_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == treino_data["nome"]
    assert data["descricao"] == treino_data["descricao"]
    assert "id" in data
    assert "usuario_id" in data


def test_read_my_treinos(client: TestClient, auth_headers):
    """Testa listagem dos treinos do usuário"""
    # Primeiro cria um treino
    treino_data = {
        "nome": "Treino Listagem",
        "descricao": "Para testar listagem"
    }
    client.post("/treinos/", headers=auth_headers, json=treino_data)
    
    # Agora lista os treinos
    response = client.get("/treinos/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["nome"] == "Treino Listagem"




def test_read_nonexistent_treino(client: TestClient, auth_headers):
    """Testa busca de treino inexistente"""
    response = client.get("/treinos/99999", headers=auth_headers)
    
    assert response.status_code == 404


def test_update_treino(client: TestClient, auth_headers):
    """Testa atualização de treino"""
    # Criar treino primeiro
    treino_data = {
        "nome": "Treino Original",
        "descricao": "Descrição original"
    }
    create_response = client.post("/treinos/", headers=auth_headers, json=treino_data)
    treino_id = create_response.json()["id"]
    
    # Atualizar o treino
    update_data = {
        "nome": "Treino Atualizado",
        "descricao": "Descrição atualizada"
    }
    response = client.put(f"/treinos/{treino_id}", headers=auth_headers, json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Treino Atualizado"
    assert data["descricao"] == "Descrição atualizada"



def test_treino_isolation_between_users(client: TestClient, db):
    """Testa que usuários não podem acessar treinos de outros usuários"""
    from app.crud.usuario import create_usuario
    from app.schemas.usuario import UsuarioCreate
    
    # Criar primeiro usuário e fazer login
    user1_data = UsuarioCreate(
        nome="User 1",
        email="user1@example.com",
        password="pass123"
    )
    user1 = create_usuario(db, user1_data)
    
    login1_data = {"username": user1.email, "password": "pass123"}
    login1_response = client.post("/auth/login", data=login1_data)
    user1_token = login1_response.json()["access_token"]
    user1_headers = {"Authorization": f"Bearer {user1_token}"}
    
    # Criar segundo usuário
    user2_data = UsuarioCreate(
        nome="User 2",
        email="user2@example.com",
        password="pass123"
    )
    user2 = create_usuario(db, user2_data)
    
    # Login do user2
    login_data = {"username": user2.email, "password": "pass123"}
    login_response = client.post("/auth/login", data=login_data)
    user2_token = login_response.json()["access_token"]
    user2_headers = {"Authorization": f"Bearer {user2_token}"}
    
    # User2 cria um treino
    treino_data = {"nome": "Treino do User2"}
    create_response = client.post("/treinos/", headers=user2_headers, json=treino_data)
    treino_id = create_response.json()["id"]
    
    # User1 tenta acessar treino do User2 (deve falhar)
    response = client.get(f"/treinos/{treino_id}", headers=user1_headers)
    assert response.status_code == 404 