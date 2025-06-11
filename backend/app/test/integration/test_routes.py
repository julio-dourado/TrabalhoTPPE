import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.main import app
from app.db.db import SessionLocal, get_db
from app.models.user import User, UserOut


@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function", autouse=True)
def clean_tables(db_session: Session):

    db_session.execute(text("""
        TRUNCATE TABLE treino_exercicio, com_peso, sem_peso, exercicios, treinos, usuarios RESTART IDENTITY CASCADE;
    """))
    db_session.commit()
    yield

@pytest.fixture(scope="function")
def client_with_db(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.mark.parametrize("user_data, expected_status_code", [
    ({"nome": "John Doe", "email": "johndoe@example.com", "senha": "securepwd123"}, 201),
    ({"nome": "John Doe", "email": "invalid-email", "senha": "securepwd123"}, 422),
    ({"nome": "J", "email": "valid@example.com", "senha": "securepwd123"}, 422),
])

def test_create_user_integration(user_data, expected_status_code, client_with_db: TestClient, db_session: Session):
    response = client_with_db.post("/user/", json=user_data)
    assert response.status_code == expected_status_code

    if expected_status_code == 201:
        created_user = response.json()
        assert "id" in created_user
        assert created_user["nome"] == user_data["nome"]
        assert created_user["email"] == user_data["email"]

        db_user = db_session.query(User).filter(User.email == user_data["email"]).first()
        assert db_user is not None
        assert db_user.nome == user_data["nome"]


def test_create_user_with_duplicate_email_fails(client_with_db: TestClient):
    user_data = {"nome": "John Doe", "email": "john.doe@unique.com", "senha": "a_strong_password"}

    response1 = client_with_db.post("/user/", json=user_data)
    assert response1.status_code == 201, "A criação inicial do usuário falhou"

    user_data2 = {"nome": "Jane Doe", "email": "john.doe@unique.com", "senha": "another_password"}
    response2 = client_with_db.post("/user/", json=user_data2)
    
    assert response2.status_code == 400, "A API não retornou 400 para e-mail duplicado"
    
    error_details = response2.json()
    assert error_details["detail"] == "Email já cadastrado"




def test_model_serialization(db_session: Session):
    test_user = User(
        nome="Test User",
        email="test@example.com",
        senha_hash="hashed_password_123"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    user_out = UserOut.model_validate(test_user)
    assert user_out.model_dump() == {
        "id": test_user.id,
        "nome": test_user.nome,
        "email": test_user.email
    }
