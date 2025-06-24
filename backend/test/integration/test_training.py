import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User as SQLAlchemyUser
from app.security.password import verify_password, get_senha_hash
from app.core.config import settings
from app.security.jwt import create_access_token, decode_token

# Note: As fixtures 'client_with_db' e 'db_session' são importadas
# automaticamente de conftest.py pelo pytest.

def test_full_authentication_flow(client_with_db: TestClient, db_session: Session):
    """
    Testa o fluxo completo de registro, login e acesso a uma rota protegida.
    """
    user_data = {
        "nome": "Test User Auth",
        "email": "testauth@example.com",
        "senha": "securepassword123"
    }

    # 1. Registrar usuário
    response_create = client_with_db.post("/api/v1/users/", json=user_data)
    assert response_create.status_code == 201
    created_user = response_create.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["nome"] == user_data["nome"]
    assert "id" in created_user

    # 2. Fazer login
    login_data = {
        "username": user_data["email"],
        "password": user_data["senha"]
    }
    response_login = client_with_db.post("/api/v1/auth/token", data=login_data)
    assert response_login.status_code == 200
    token_data = response_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

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

    login_data = {
        "username": user_data.email,
        "password": "wrongpassword"
    }
    response = client_with_db.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Credenciais inválidas"

def test_access_protected_route_without_token_fails(client_with_db: TestClient):
    """
    Testa que o acesso a rota protegida sem token falha.
    """
    response = client_with_db.get("/api/v1/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_access_protected_route_with_invalid_token_fails(client_with_db: TestClient):
    """
    Testa que o acesso a rota protegida com token inválido falha.
    """
    headers = {"Authorization": "Bearer invalid.token.string"}
    response = client_with_db.get("/api/v1/users/me/", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_update_user_me(client_with_authenticated_user: TestClient, db_session: Session, authenticated_user: SQLAlchemyUser):
    """
    Testa a atualização dos dados do próprio usuário autenticado.
    """
    headers = {"Authorization": "Bearer fake-token"}
    
    update_data = {
        "nome": "Updated Name",
        "email": "updated@example.com",
        "senha": "newsecurepassword"
    }

    response = client_with_authenticated_user.put("/api/v1/users/me/", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_user_response = response.json()

    assert updated_user_response["nome"] == "Updated Name"
    assert updated_user_response["email"] == "updated@example.com"
    assert updated_user_response["id"] == authenticated_user.id

    # Verifica no banco de dados se a senha foi hashada corretamente
    db_user = db_session.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == authenticated_user.id).first()
    assert db_user is not None
    assert db_user.nome == "Updated Name"
    assert db_user.email == "updated@example.com"
    assert verify_password("newsecurepassword", db_user.senha_hash)

def test_update_user_me_email_already_exists(client_with_authenticated_user: TestClient, db_session: Session, authenticated_user: SQLAlchemyUser):
    """
    Testa a tentativa de atualizar o e-mail para um que já existe.
    """
    headers = {"Authorization": "Bearer fake-token"}

    # Cria um segundo usuário para ter um e-mail existente
    other_user_data = {
        "nome": "Existing Email User",
        "email": "existing@example.com",
        "senha_hash": get_senha_hash("somepass")
    }
    other_user = SQLAlchemyUser(**other_user_data)
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    update_data = {
        "nome": "New Name",
        "email": "existing@example.com",
        "senha": "newpassword"
    }

    response = client_with_authenticated_user.put("/api/v1/users/me/", json=update_data, headers=headers)
    assert response.status_code == 400
    assert "Um usuário com este novo e-mail já existe." in response.json()["detail"]

def test_delete_user_me(client_with_authenticated_user: TestClient, db_session: Session, authenticated_user: SQLAlchemyUser):
    """
    Testa a deleção do próprio usuário autenticado.
    """
    headers = {"Authorization": "Bearer fake-token"}

    response = client_with_authenticated_user.delete("/api/v1/users/me/", headers=headers)
    assert response.status_code == 204

    # Verifica se o usuário foi realmente deletado do DB
    deleted_user = db_session.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == authenticated_user.id).first()
    assert deleted_user is None

def test_delete_user_me_not_found_after_deletion(client_with_authenticated_user: TestClient, db_session: Session, authenticated_user: SQLAlchemyUser):
    """
    Testa que uma tentativa de deletar um usuário já deletado retorna 404.
    """
    headers = {"Authorization": "Bearer fake-token"}

    # Deleta o usuário uma vez
    response_delete = client_with_authenticated_user.delete("/api/v1/users/me/", headers=headers)
    assert response_delete.status_code == 204

    # Tenta deletar novamente
    response_delete_again = client_with_authenticated_user.delete("/api/v1/users/me/", headers=headers)
    assert response_delete_again.status_code == 404
    assert "Usuário não encontrado." in response_delete_again.json()["detail"]

