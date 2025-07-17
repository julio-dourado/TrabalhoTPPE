import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.db.session import Base, get_db
from app.core.config import settings
from app.models import User, Training, Exercise  # Import models to ensure they're registered
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.api.deps import get_current_user


@pytest.fixture(scope="session")
def engine():
    """Create a test database engine"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db(engine):
    """Create a test database session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Start a transaction
    connection = engine.connect()
    transaction = connection.begin()
    
    # Bind the session to the connection
    session.bind = connection
    
    yield session
    
    # Rollback the transaction and close the session
    transaction.rollback()
    connection.close()
    session.close()


@pytest.fixture(scope="function")
def clean_db(db):
    """Clean database before each test"""
    # Delete all records from all tables
    db.query(User).delete()
    db.query(Training).delete()
    db.query(Exercise).delete()
    db.commit()
    
    return db


@pytest.fixture(scope="function")
def authenticated_user(db_session: Session) -> User:
    """
    Cria um usuário autenticado para os testes.
    """
    user_data = UserCreate(
        nome="Usuário Autenticado",
        email="autenticado@example.com",
        senha="senha_segura_123",
    )
    user = create_user(db_session, user_data)
    return user


@pytest.fixture
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


@pytest.fixture(scope="function")
def client_with_authenticated_user(
    db_session: Session, authenticated_user: User
) -> TestClient:
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return authenticated_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
