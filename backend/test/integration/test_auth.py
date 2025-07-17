import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User as SQLAlchemyUser
from app.security.password import verify_password, get_senha_hash
from app.core.config import settings
from app.security.jwt import create_access_token, decode_token
from app.services import user_service


def test_full_authentication_flow(client_with_db: TestClient, db_session: Session):
    user_data = {
        "nome": "Usuário de Teste Auth",
        "email": "auth.test@exemplo.com",
        "senha": "senha_super_segura_123",
    }
    response_create = client_with_db.post("/api/v1/users/", json=user_data)
    assert (
        response_create.status_code == 201
    ), "Falha ao criar usuário para o teste de login"
    created_user = response_create.json()

    login_data = {"username": user_data["email"], "password": user_data["senha"]}
    response_login = client_with_db.post("/api/v1/auth/token", data=login_data)

    assert response_login.status_code == 200, "O login falhou com credenciais corretas"
    token_info = response_login.json()
    assert "access_token" in token_info
    assert token_info["token_type"] == "bearer"

    access_token = token_info["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_me = client_with_db.get("/api/v1/users/me/", headers=headers)

    assert (
        response_me.status_code == 200
    ), "Falha ao acessar a rota protegida com um token válido"
    profile_data = response_me.json()
    assert profile_data["email"] == user_data["email"]
    assert profile_data["id"] == created_user["id"]


def test_login_with_wrong_password_fails(
    client_with_db: TestClient, db_session: Session
):
    user_data_for_creation = UserCreate(
        nome="Usuário Senha Errada",
        email="wrong.password@exemplo.com",
        senha="senha_correta",
    )
    user_service.create_user(db_session, user_data_for_creation)

    login_data = {
        "username": user_data_for_creation.email,
        "password": "senha_errada_propositalmente",
    }
    response_login = client_with_db.post("/api/v1/auth/token", data=login_data)

    assert response_login.status_code == 400
    assert response_login.json()["detail"] == "Credenciais inválidas"


def test_access_protected_route_without_token_fails(client_with_db: TestClient):
    response = client_with_db.get("/api/v1/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_access_protected_route_with_invalid_token_fails(client_with_db: TestClient):
    headers = {"Authorization": "Bearer token_falso_e_invalido"}
    response = client_with_db.get("/api/v1/users/me/", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_update_user_me(
    client_with_authenticated_user: TestClient,
    db_session: Session,
    authenticated_user: SQLAlchemyUser,
):
    """
    Testa a atualização dos dados do próprio usuário autenticado.
    """
    headers = {"Authorization": "Bearer fake-token"}

    update_data = {
        "nome": "Updated Name",
        "email": "updated@example.com",
        "senha": "newsecurepassword",
    }

    response = client_with_authenticated_user.put(
        "/api/v1/users/me/", json=update_data, headers=headers
    )
    assert response.status_code == 200
    updated_user_response = response.json()

    assert updated_user_response["nome"] == "Updated Name"
    assert updated_user_response["email"] == "updated@example.com"
    assert updated_user_response["id"] == authenticated_user.id

    # Verifica no banco de dados se a senha foi hashada corretamente
    db_user = (
        db_session.query(SQLAlchemyUser)
        .filter(SQLAlchemyUser.id == authenticated_user.id)
        .first()
    )
    assert db_user is not None
    assert db_user.nome == "Updated Name"
    assert db_user.email == "updated@example.com"
    assert verify_password("newsecurepassword", db_user.senha_hash)


def test_update_user_me_email_already_exists(
    client_with_authenticated_user: TestClient,
    db_session: Session,
    authenticated_user: SQLAlchemyUser,
):
    """
    Testa a tentativa de atualizar o e-mail para um que já existe.
    """
    headers = {"Authorization": "Bearer fake-token"}

    # Cria um segundo usuário para ter um e-mail existente
    other_user_data_for_creation = UserCreate(
        nome="Existing Email User", email="existing@example.com", senha="somepass"
    )
    user_service.create_user(db_session, other_user_data_for_creation)

    update_data = {
        "nome": "New Name",
        "email": "existing@example.com",
        "senha": "newpassword",
    }

    response = client_with_authenticated_user.put(
        "/api/v1/users/me/", json=update_data, headers=headers
    )
    assert response.status_code == 400
    assert "Um usuário com este novo e-mail já existe." in response.json()["detail"]


def test_delete_user_me(
    client_with_authenticated_user: TestClient,
    db_session: Session,
    authenticated_user: SQLAlchemyUser,
):
    """
    Testa a deleção do próprio usuário autenticado.
    """
    headers = {"Authorization": "Bearer fake-token"}

    response = client_with_authenticated_user.delete(
        "/api/v1/users/me/", headers=headers
    )
    assert response.status_code == 204

    # Verifica se o usuário foi realmente deletado do DB
    deleted_user = (
        db_session.query(SQLAlchemyUser)
        .filter(SQLAlchemyUser.id == authenticated_user.id)
        .first()
    )
    assert deleted_user is None


def test_delete_user_me_not_found_after_deletion(
    client_with_authenticated_user: TestClient,
    db_session: Session,
    authenticated_user: SQLAlchemyUser,
):
    """
    Testa que uma tentativa de deletar um usuário já deletado retorna 404.
    """
    headers = {"Authorization": "Bearer fake-token"}

    # Deleta o usuário uma vez
    response_delete = client_with_authenticated_user.delete(
        "/api/v1/users/me/", headers=headers
    )
    assert response_delete.status_code == 204

    # Tenta deletar novamente
    response_delete_again = client_with_authenticated_user.delete(
        "/api/v1/users/me/", headers=headers
    )
    assert response_delete_again.status_code == 404
    assert "Usuário não encontrado." in response_delete_again.json()["detail"]
