from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from sqlalchemy.schema import MetaData # Importa MetaData
from sqlmodel import SQLModel # Importa SQLModel para configurar seu metadata

# Convenção para nomear restrições (útil para migrations)
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Define o objeto MetaData compartilhado
# Todos os modelos (SQLAlchemy e SQLModel) usarão este MetaData.
shared_metadata = MetaData(naming_convention=convention)

# Configura o SQLModel para usar o MetaData compartilhado
# Esta linha é crucial para que SQLModel registre suas tabelas no MetaData do SQLAlchemy
SQLModel.metadata = shared_metadata

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://appuser:secret@db:5432/appdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=shared_metadata) # Passa o objeto MetaData compartilhado aqui

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# init_db não é mais estritamente necessário se usar migrations, mas mantemos para clareza
# que Base.metadata.create_all() criará tudo.
def init_db():
    Base.metadata.create_all(bind=engine)

