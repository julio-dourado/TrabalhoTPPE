import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.db import Base, get_db
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação das tabelas no banco de dados de teste
@pytest.fixture(scope="module")
def setup_db():
    
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()  # Fornece uma sessão para os testes
    # Limpa as tabelas após os testes
    Base.metadata.drop_all(bind=engine)

# Fixture para obter a sessão do banco de dados
@pytest.fixture
def db_session(setup_db):
    return setup_db
