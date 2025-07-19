#!/usr/bin/env python3
"""
Script para configurar o banco de dados automaticamente
Pode ser usado localmente ou no deploy da AWS
"""

import os
import sys
import logging
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from app.config import settings
from app.database import Base
from app.models import usuario, treino, exercicio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database():
    """Cria o banco de dados se não existir"""
    try:
        # Parse database URL to get connection info
        from urllib.parse import urlparse
        parsed = urlparse(settings.database_url)
        
        # Connect to postgres database to create our database
        postgres_url = f"postgresql://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}/postgres"
        engine = create_engine(postgres_url)
        
        db_name = parsed.path[1:]  # Remove leading slash
        
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"), 
                {"db_name": db_name}
            )
            
            if not result.fetchone():
                # Create database
                conn.execute(text("COMMIT"))  # End current transaction
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                logger.info(f"✅ Banco de dados '{db_name}' criado com sucesso!")
            else:
                logger.info(f"ℹ️  Banco de dados '{db_name}' já existe.")
                
    except Exception as e:
        logger.error(f"❌ Erro ao criar banco de dados: {e}")
        logger.info("Tentando continuar com as tabelas...")


def create_tables():
    """Cria as tabelas usando SQLAlchemy"""
    try:
        engine = create_engine(settings.database_url)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas criadas com sucesso!")
        
        return engine
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        return None


def load_sql_file(engine, sql_file_path):
    """Carrega e executa arquivo SQL"""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        with engine.connect() as conn:
            for stmt in statements:
                if stmt.strip():
                    try:
                        conn.execute(text(stmt))
                    except Exception as e:
                        # Some statements might fail if data already exists
                        logger.warning(f"⚠️  Statement skipped: {str(e)[:100]}...")
            conn.commit()
            
        logger.info(f"✅ Arquivo SQL carregado: {sql_file_path}")
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar arquivo SQL: {e}")


def create_admin_user(engine):
    """Cria usuário administrador inicial"""
    try:
        from app.crud.usuario import create_usuario, get_usuario_by_email
        from app.schemas.usuario import UsuarioCreate
        from app.database import SessionLocal
        
        db = SessionLocal()
        
        # Check if admin exists
        admin_email = "admin@treino.com"
        existing_admin = get_usuario_by_email(db, admin_email)
        
        if not existing_admin:
            admin_data = UsuarioCreate(
                nome="Administrador",
                email=admin_email,
                password="admin123"  # Change this!
            )
            create_usuario(db, admin_data)
            logger.info("✅ Usuário administrador criado!")
            logger.warning(f"⚠️  Email: {admin_email} | Senha: admin123")
            logger.warning("⚠️  MUDE A SENHA APÓS O PRIMEIRO LOGIN!")
        else:
            logger.info("ℹ️  Usuário administrador já existe.")
            
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar usuário admin: {e}")


def main():
    """Função principal"""
    logger.info("🚀 Configurando banco de dados...")
    
    # 1. Create database
    create_database()
    
    # 2. Create tables
    engine = create_tables()
    if not engine:
        logger.error("❌ Falha ao criar tabelas. Abortando.")
        return
    
    # 3. Load sample data if in development
    if settings.database_url.startswith("sqlite") or "localhost" in settings.database_url:
        seed_file = Path(__file__).parent.parent / "database" / "seed_data.sql"
        if seed_file.exists():
            load_sql_file(engine, str(seed_file))
        else:
            logger.info("ℹ️  Criando usuário administrador...")
            create_admin_user(engine)
    
    logger.info("🎉 Configuração do banco de dados concluída!")
    logger.info("📖 Acesse a documentação em: http://localhost:8000/docs")


if __name__ == "__main__":
    main() 