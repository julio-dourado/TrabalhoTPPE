#!/usr/bin/env python3
"""
Script auxiliar para deploy na AWS
Verifica configurações e prepara ambiente
"""

import os
import sys
import logging
import boto3
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_aws_credentials():
    """Verifica credenciais AWS"""
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if not credentials:
            logger.error("❌ Credenciais AWS não encontradas!")
            logger.info("Configure com: aws configure")
            return False
            
        logger.info("✅ Credenciais AWS encontradas")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar credenciais: {e}")
        return False


def check_rds_connection():
    """Verifica conexão com RDS"""
    try:
        from app.config import settings
        from sqlalchemy import create_engine
        
        if "amazonaws.com" not in settings.database_url:
            logger.warning("⚠️  URL do banco não parece ser AWS RDS")
            return False
            
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info("✅ Conexão com RDS estabelecida")
            return True
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com RDS: {e}")
        return False


def generate_requirements_lock():
    """Gera requirements com versões fixas"""
    try:
        import subprocess
        
        logger.info("📦 Gerando requirements com versões fixas...")
        result = subprocess.run(
            ["pip", "freeze"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if result.returncode == 0:
            lock_file = Path(__file__).parent.parent / "requirements-lock.txt"
            with open(lock_file, 'w') as f:
                f.write(result.stdout)
            logger.info(f"✅ requirements-lock.txt criado")
        else:
            logger.error("❌ Erro ao gerar requirements")
            
    except Exception as e:
        logger.error(f"❌ Erro: {e}")


def validate_environment():
    """Valida variáveis de ambiente"""
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "ACCESS_TOKEN_EXPIRE_MINUTES"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        logger.error(f"❌ Variáveis de ambiente faltando: {missing}")
        return False
    
    # Check SECRET_KEY strength
    secret_key = os.getenv("SECRET_KEY")
    if len(secret_key) < 32:
        logger.warning("⚠️  SECRET_KEY deve ter pelo menos 32 caracteres")
    
    logger.info("✅ Variáveis de ambiente validadas")
    return True


def create_docker_compose_prod():
    """Cria docker-compose para produção"""
    compose_content = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
      - ENVIRONMENT=production
    command: >
      sh -c "python scripts/setup_database.py &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  default:
    name: treino-network
"""
    
    compose_file = Path(__file__).parent.parent / "docker-compose.prod.yml"
    with open(compose_file, 'w') as f:
        f.write(compose_content)
    
    logger.info("✅ docker-compose.prod.yml criado")


def main():
    """Função principal"""
    logger.info("🚀 Preparando deploy AWS...")
    
    # Verificações
    checks_passed = True
    
    if not validate_environment():
        checks_passed = False
    
    if not check_aws_credentials():
        checks_passed = False
    
    # Preparações
    generate_requirements_lock()
    create_docker_compose_prod()
    
    if checks_passed:
        logger.info("🎉 Ambiente pronto para deploy!")
        logger.info("\n📋 Próximos passos:")
        logger.info("1. Configure seu RDS PostgreSQL na AWS")
        logger.info("2. Configure ECS/EC2/Elastic Beanstalk")
        logger.info("3. Execute: docker-compose -f docker-compose.prod.yml up -d")
    else:
        logger.error("❌ Corrija os problemas antes do deploy")


if __name__ == "__main__":
    main() 