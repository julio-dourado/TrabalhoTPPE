"""
Script para inicializar o banco de dados
Cria as tabelas e pode inserir dados iniciais se necessário
"""
import logging
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models.usuario import Usuario
from .models.treino import Treino
from .models.exercicio import Exercicio
from .crud.usuario import create_usuario, get_usuario_by_email
from .schemas.usuario import UsuarioCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables() -> None:
    """Cria todas as tabelas"""
    Usuario.metadata.create_all(bind=engine)
    Treino.metadata.create_all(bind=engine)
    Exercicio.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso")


def create_initial_user() -> None:
    """Cria usuário inicial para testes"""
    db: Session = SessionLocal()
    try:
        # Verifica se já existe
        existing_user = get_usuario_by_email(db, email="admin@test.com")
        if not existing_user:
            user_data = UsuarioCreate(
                nome="Admin Test",
                email="admin@test.com",
                password="123456"
            )
            create_usuario(db, user_data)
            logger.info("Usuário inicial criado: admin@test.com")
        else:
            logger.info("Usuário inicial já existe")
    except Exception as e:
        logger.error(f"Erro ao criar usuário inicial: {e}")
    finally:
        db.close()


def init_db() -> None:
    """Inicializa o banco de dados"""
    logger.info("Inicializando banco de dados...")
    create_tables()
    create_initial_user()
    logger.info("Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    init_db() 