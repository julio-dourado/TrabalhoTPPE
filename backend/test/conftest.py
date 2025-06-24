import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.db.session import Base, get_db
from app.core.config import settings
from app.models.user import User as SQLAlchemyUser
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.api.v1.deps import get_current_user

engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(scope="function")
def db_session() -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function", autouse=True)
def clean_tables(db_session: Session):
    try:
        db_session.execute(text("DELETE FROM treinoexerciciolink"))
    except:
        pass
    try:
        db_session.execute(text("DELETE FROM compeso"))
    except:
        pass
    try:
        db_session.execute(text("DELETE FROM sempeso"))
    except:
        pass
    try:
        db_session.execute(text("DELETE FROM exercicio"))
    except:
        pass
    try:
        db_session.execute(text("DELETE FROM treino"))
    except:
        pass
    try:
        db_session.execute(text("DELETE FROM usuarios"))
    except:
        pass
    db_session.commit()

@pytest.fixture(scope="function")
def authenticated_user(db_session: Session) -> SQLAlchemyUser:
    """
    Cria um usuário autenticado para os testes.
    """
    user_data = UserCreate(
        nome="Usuário Autenticado",
        email="autenticado@example.com",
        senha="senha_segura_123"
    )
    user = create_user(db_session, user_data)
    return user

@pytest.fixture(scope="function")
def client_with_db(db_session: Session) -> TestClient:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client_with_authenticated_user(db_session: Session, authenticated_user: SQLAlchemyUser) -> TestClient:
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return authenticated_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
