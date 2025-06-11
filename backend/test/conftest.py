import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_db():
    
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    # Limpa as tabelas após os testes
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_db):
    return setup_db
