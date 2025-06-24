import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User as SQLAlchemyUser
from app.security.password import verify_password, get_senha_hash
from app.core.config import settings
from app.security.jwt import create_access_token, decode_token
from app.schemas.training import TreinoCreate
from app.schemas.exercise import ExercicioCreate, ComPesoCreate, SemPesoCreate

# Note: As fixtures 'client_with_db' e 'db_session' são importadas
# automaticamente de conftest.py pelo pytest.

def test_full_authentication_flow(client_with_db: TestClient, db_session: Session):
    """
    Testa o fluxo completo de registro, login e acesso a uma rota protegida.
    """
    user_data = {
        "nome": "Test User",
        "email": "test@example.com",
        "senha": "password123"
    }

    # 1. Registrar usuário
    response_create = client_with_db.post("/api/v1/users/", json=user_data)
    assert response_create.status_code == 201
    created_user = response_create.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["nome"] == user_data["nome"]
    assert "id" in created_user

    # 2. Fazer login
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Acessar rota protegida (/users/me)
    response_me = client_with_db.get("/api/v1/users/me/", headers=headers)
    assert response_me.status_code == 200
    me_user = response_me.json()
    assert me_user["email"] == user_data["email"]
    assert me_user["nome"] == user_data["nome"]
    assert me_user["id"] == created_user["id"]

def test_login_with_wrong_password_fails(client_with_db: TestClient, db_session: Session):
    """
    Testa que o login falha com senha incorreta.
    """
    user_data = UserCreate(
        nome="Wrong Pass User",
        email="wrongpass@example.com",
        senha="correctpassword"
    )
    from app.services.user_service import create_user
    create_user(db_session, user_data)

    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": user_data.email,
        "password": "wrongpassword"
    })
    assert response_login.status_code == 400

def test_access_protected_route_without_token_fails(client_with_db: TestClient, db_session: Session):
    """
    Testa que o acesso a rota protegida sem token falha.
    """
    response = client_with_db.get("/api/v1/users/me/")
    assert response.status_code == 401

def test_access_protected_route_with_invalid_token_fails(client_with_db: TestClient, db_session: Session):
    """
    Testa que o acesso a rota protegida com token inválido falha.
    """
    headers = {"Authorization": "Bearer invalid_token"}
    response = client_with_db.get("/api/v1/users/me/", headers=headers)
    assert response.status_code == 401

def test_update_user_me(client_with_db: TestClient, db_session: Session):
    """
    Testa a atualização dos dados do próprio usuário autenticado.
    """
    user_data = {
        "nome": "Test User",
        "email": "test3@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test3@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"nome": "Updated Name"}
    response_update = client_with_db.put("/api/v1/users/me/", json=update_data, headers=headers)
    assert response_update.status_code == 200
    assert response_update.json()["nome"] == "Updated Name"

def test_update_user_me_email_already_exists(client_with_db: TestClient, db_session: Session):
    """
    Testa a tentativa de atualizar o e-mail para um que já existe.
    """
    user1_data = {
        "nome": "User 1",
        "email": "user1@example.com",
        "senha": "password123"
    }
    user2_data = {
        "nome": "User 2",
        "email": "user2@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user1_data)
    client_with_db.post("/api/v1/users/", json=user2_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "user1@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"email": "user2@example.com"}
    response_update = client_with_db.put("/api/v1/users/me/", json=update_data, headers=headers)
    assert response_update.status_code == 400

def test_delete_user_me(client_with_db: TestClient, db_session: Session):
    """
    Testa a deleção do próprio usuário autenticado.
    """
    user_data = {
        "nome": "Test User",
        "email": "test4@example.com",
        "senha": "password123"
    }
    
    create_response = client_with_db.post("/api/v1/users/", json=user_data)
    created_user = create_response.json()
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test4@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response_delete = client_with_db.delete("/api/v1/users/me/", headers=headers)
    assert response_delete.status_code == 204

    deleted_user = db_session.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == created_user["id"]).first()
    assert deleted_user is None

def test_delete_user_me_not_found_after_deletion(client_with_db: TestClient, db_session: Session):
    """
    Testa que uma tentativa de deletar um usuário já deletado retorna 404.
    """
    user_data = {
        "nome": "Test User",
        "email": "test5@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test5@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    client_with_db.delete("/api/v1/users/me/", headers=headers)
    
    response_me = client_with_db.get("/api/v1/users/me/", headers=headers)
    assert response_me.status_code == 401

def test_create_training_with_weight_exercises(client_with_db: TestClient, db_session: Session):
    """
    US07: Eu, como usuário, gostaria de criar um treino com exercícios personalizados.
    US11: Eu, como usuário, gostaria de criar exercícios com peso, informando nome, músculo, repetições, sets e carga.
    """
    user_data = {
        "nome": "Test User",
        "email": "test6@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test6@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    training_data = {
        "nome": "Treino Teste",
        "exercicios": [
            {
                "nome": "Supino",
                "serie": 4,
                "repeticoes": 8,
                "comentario": "Teste",
                "tipo_exercicio": "ComPeso",
                "com_peso_details": {
                    "peso": 80.0
                }
            }
        ]
    }
    
    response = client_with_db.post("/api/v1/treinos/", json=training_data, headers=headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["nome"] == "Treino Teste"
    assert len(data["exercicios"]) == 1
    assert data["exercicios"][0]["nome"] == "Supino"
    assert data["exercicios"][0]["tipo_exercicio"] == "ComPeso"
    assert data["exercicios"][0]["com_peso_details"]["peso"] == 80.0

def test_create_training_with_cardio_exercises(client_with_db: TestClient, db_session: Session):
    """
    US14: Eu, como usuário, gostaria de criar exercícios sem peso, informando nome, tempo e distância.
    """
    user_data = {
        "nome": "Test User",
        "email": "test7@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test7@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    training_data = {
        "nome": "Treino Cardio",
        "exercicios": [
            {
                "nome": "Corrida",
                "serie": 1,
                "repeticoes": 1,
                "comentario": "Cardio",
                "tipo_exercicio": "SemPeso",
                "sem_peso_details": {
                    "tempo_seg": 1800.0,
                    "distancia_m": 5000.0,
                    "meta_velocidade": 2.8
                }
            }
        ]
    }
    
    response = client_with_db.post("/api/v1/treinos/", json=training_data, headers=headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["nome"] == "Treino Cardio"
    assert len(data["exercicios"]) == 1
    assert data["exercicios"][0]["nome"] == "Corrida"
    assert data["exercicios"][0]["tipo_exercicio"] == "SemPeso"
    assert data["exercicios"][0]["sem_peso_details"]["tempo_seg"] == 1800.0

def test_get_user_trainings(client_with_db: TestClient, db_session: Session):
    """
    US08: Eu, como usuário, gostaria de visualizar os treinos criados.
    US17: Eu, como usuário, gostaria de visualizar uma lista de treinos e selecionar um para ver os detalhes.
    """
    user_data = {
        "nome": "Test User",
        "email": "test8@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test8@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    training_data = {
        "nome": "Treino Teste",
        "exercicios": [
            {
                "nome": "Flexão",
                "serie": 3,
                "repeticoes": 10,
                "comentario": "Exercício básico",
                "tipo_exercicio": "SemPeso",
                "sem_peso_details": {
                    "tempo_seg": 300.0,
                    "distancia_m": 0.0,
                    "meta_velocidade": 1.0
                }
            }
        ]
    }
    
    create_response = client_with_db.post("/api/v1/treinos/", json=training_data, headers=headers)
    assert create_response.status_code == 201
    
    response = client_with_db.get("/api/v1/treinos/", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["nome"] == "Treino Teste"

def test_get_specific_training_details(client_with_db: TestClient, db_session: Session):
    """
    US18: Eu, como usuário, gostaria de visualizar os detalhes de um treino com todos os exercícios listados.
    """
    user_data = {
        "nome": "Test User",
        "email": "test9@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test9@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    training_data = {
        "nome": "Treino Teste",
        "exercicios": [
            {
                "nome": "Supino",
                "serie": 4,
                "repeticoes": 8,
                "comentario": "Teste",
                "tipo_exercicio": "ComPeso",
                "com_peso_details": {
                    "peso": 80.0
                }
            }
        ]
    }
    
    create_response = client_with_db.post("/api/v1/treinos/", json=training_data, headers=headers)
    assert create_response.status_code == 201
    training_id = create_response.json()["id"]
    
    response = client_with_db.get(f"/api/v1/treinos/{training_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["nome"] == "Treino Teste"
    assert len(data["exercicios"]) == 1
    assert data["exercicios"][0]["nome"] == "Supino"

def test_update_training(client_with_db: TestClient, db_session: Session):
    """
    US09: Eu, como usuário, gostaria de editar um treino existente.
    """
    user_data = {
        "nome": "Test User",
        "email": "test10@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test10@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    training_data = {
        "nome": "Treino Original",
        "exercicios": [
            {
                "nome": "Flexão",
                "serie": 3,
                "repeticoes": 10,
                "comentario": "Exercício básico",
                "tipo_exercicio": "SemPeso",
                "sem_peso_details": {
                    "tempo_seg": 300.0,
                    "distancia_m": 0.0,
                    "meta_velocidade": 1.0
                }
            }
        ]
    }
    
    create_response = client_with_db.post("/api/v1/treinos/", json=training_data, headers=headers)
    training_id = create_response.json()["id"]
    
    update_data = {"nome": "Treino Atualizado"}
    response = client_with_db.put(f"/api/v1/treinos/{training_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["nome"] == "Treino Atualizado"

def test_delete_training(client_with_db: TestClient, db_session: Session):
    """
    US10: Eu, como usuário, gostaria de excluir um treino.
    """
    user_data = {
        "nome": "Test User",
        "email": "test11@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test11@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    training_data = {
        "nome": "Treino para Deletar",
        "exercicios": [
            {
                "nome": "Flexão",
                "serie": 3,
                "repeticoes": 10,
                "comentario": "Exercício básico",
                "tipo_exercicio": "SemPeso",
                "sem_peso_details": {
                    "tempo_seg": 300.0,
                    "distancia_m": 0.0,
                    "meta_velocidade": 1.0
                }
            }
        ]
    }
    
    create_response = client_with_db.post("/api/v1/treinos/", json=training_data, headers=headers)
    assert create_response.status_code == 201
    training_id = create_response.json()["id"]
    
    response = client_with_db.delete(f"/api/v1/treinos/{training_id}", headers=headers)
    assert response.status_code == 204

def test_create_training_unauthorized(client_with_db: TestClient, db_session: Session):
    """
    Testa que criar treino sem autenticação falha.
    """
    training_data = {
        "nome": "Treino Teste",
        "exercicios": [
            {
                "nome": "Flexão",
                "serie": 3,
                "repeticoes": 10,
                "comentario": "Exercício básico",
                "tipo_exercicio": "SemPeso",
                "sem_peso_details": {
                    "tempo_seg": 300.0,
                    "distancia_m": 0.0,
                    "meta_velocidade": 1.0
                }
            }
        ]
    }
    
    response = client_with_db.post("/api/v1/treinos/", json=training_data)
    assert response.status_code == 401

def test_access_other_user_training_fails(client_with_db: TestClient, db_session: Session):
    """
    Testa que um usuário não pode acessar treinos de outros usuários.
    """
    user1_data = {
        "nome": "User 1",
        "email": "user1@example.com",
        "senha": "password123"
    }
    user2_data = {
        "nome": "User 2",
        "email": "user2@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user1_data)
    client_with_db.post("/api/v1/users/", json=user2_data)
    
    response_login1 = client_with_db.post("/api/v1/auth/token", data={
        "username": "user1@example.com",
        "password": "password123"
    })
    token1 = response_login1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    
    response_login2 = client_with_db.post("/api/v1/auth/token", data={
        "username": "user2@example.com",
        "password": "password123"
    })
    token2 = response_login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    training_data = {
        "nome": "Treino User 1",
        "exercicios": [
            {
                "nome": "Flexão",
                "serie": 3,
                "repeticoes": 10,
                "comentario": "Exercício básico",
                "tipo_exercicio": "SemPeso",
                "sem_peso_details": {
                    "tempo_seg": 300.0,
                    "distancia_m": 0.0,
                    "meta_velocidade": 1.0
                }
            }
        ]
    }
    
    create_response = client_with_db.post("/api/v1/treinos/", json=training_data, headers=headers1)
    assert create_response.status_code == 201
    training_id = create_response.json()["id"]
    
    response = client_with_db.get(f"/api/v1/treinos/{training_id}", headers=headers2)
    assert response.status_code == 404

def test_create_training_validation_errors(client_with_db: TestClient, db_session: Session):
    """
    Testa validações de entrada para criação de treinos.
    """
    user_data = {
        "nome": "Test User",
        "email": "test12@example.com",
        "senha": "password123"
    }
    
    client_with_db.post("/api/v1/users/", json=user_data)
    
    response_login = client_with_db.post("/api/v1/auth/token", data={
        "username": "test12@example.com",
        "password": "password123"
    })
    token = response_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    invalid_training_data = {
        "nome": "",
        "exercicios": [
            {
                "nome": "Supino",
                "serie": -1,
                "repeticoes": 0,
                "tipo_exercicio": "ComPeso",
                "com_peso_details": {
                    "peso": -10.0
                }
            }
        ]
    }
    
    response = client_with_db.post("/api/v1/treinos/", json=invalid_training_data, headers=headers)
    assert response.status_code == 422

