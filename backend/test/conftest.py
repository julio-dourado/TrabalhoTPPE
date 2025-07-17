import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.db.session import Base, get_db
from app.core.config import Settings
from app.models import User, Training, Exercise  # Import models to ensure they're registered
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.api.deps import get_current_user

settings = Settings()

# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables for the test
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a test database session"""
    # Drop all tables first
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    
    yield session
    
    # Close the session
    session.close()


@pytest.fixture(scope="function")
def authenticated_user(db: Session) -> User:
    """
    Create an authenticated user for tests.
    """
    user_data = UserCreate(
        name="Authenticated User",
        email="authenticated@example.com",
        password="secure_password_123",
    )
    user = UserService.create_user(db, user_data)
    return user


@pytest.fixture
def client_with_db(db: Session):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_with_authenticated_user(
    db: Session, authenticated_user: User
) -> TestClient:
    def override_get_db():
        yield db

    def override_get_current_user():
        return authenticated_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
