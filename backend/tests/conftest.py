import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.main import app
from app.database import get_db, Base
from app.crud.usuario import create_usuario
from app.schemas.usuario import UsuarioCreate

# Usar banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override do banco de dados para testes"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override da dependência
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    """Fixture do banco de dados para testes"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Cliente de teste do FastAPI"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(db):
    """Cria usuário de teste"""
    user_data = UsuarioCreate(
        nome="Test User",
        email="test@example.com",
        password="testpass123"
    )
    return create_usuario(db, user_data)


@pytest.fixture
def auth_headers(client, test_user):
    """Headers de autenticação para testes"""
    login_data = {
        "username": test_user.email,
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"} 