# app/core/config.py
import os
from typing import Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação com validação e suporte a múltiplos ambientes"""
    
    # Configurações da aplicação
    APP_NAME: str = "API de Treinos"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", description="Ambiente de execução")
    DEBUG: bool = Field(default=False, description="Modo debug")
    
    # Configurações do banco de dados
    POSTGRES_USER: str = Field(default="test_user", description="Usuário do PostgreSQL")
    POSTGRES_PASSWORD: str = Field(default="test_password", description="Senha do PostgreSQL")
    POSTGRES_DB: str = Field(default="test_db", description="Nome do banco PostgreSQL")
    POSTGRES_HOST: str = Field(default="localhost", description="Host do PostgreSQL")
    POSTGRES_PORT: int = Field(default=5432, description="Porta do PostgreSQL")
    
    # URL do banco (calculada automaticamente)
    DATABASE_URL: Optional[str] = None
    
    # Configurações de segurança
    SECRET_KEY: str = Field(
        default="dev_secret_key_change_in_production",
        min_length=32,
        description="Chave secreta para JWT"
    )
    ALGORITHM: str = Field(default="HS256", description="Algoritmo de criptografia")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, 
        ge=1, 
        le=10080,  # máximo 1 semana
        description="Tempo de expiração do token em minutos"
    )
    
    # Configurações de CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Origens permitidas para CORS"
    )
    
    # Configurações de logging
    LOG_LEVEL: str = Field(default="INFO", description="Nível de log")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Formato do log"
    )
    
    # Configurações de arquivo
    UPLOAD_DIR: str = Field(default="uploads", description="Diretório de uploads")
    MAX_FILE_SIZE: int = Field(default=10_000_000, description="Tamanho máximo de arquivo em bytes")
    
    @validator("DATABASE_URL", pre=True, always=True)
    def build_database_url(cls, v, values):
        """Constrói a URL do banco automaticamente se não fornecida"""
        if v:
            return v
        
        environment = values.get("ENVIRONMENT", "development")
        
        if environment == "test":
            return "sqlite:///./test.db"
        elif environment == "development":
            return "sqlite:///./development.db"
        else:
            # Produção usa PostgreSQL
            user = values.get("POSTGRES_USER")
            password = values.get("POSTGRES_PASSWORD")
            host = values.get("POSTGRES_HOST")
            port = values.get("POSTGRES_PORT")
            db = values.get("POSTGRES_DB")
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Valida se o ambiente é válido"""
        allowed_envs = ["development", "test", "staging", "production"]
        if v not in allowed_envs:
            raise ValueError(f"Environment deve ser um de: {allowed_envs}")
        return v
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v, values):
        """Valida a chave secreta em produção"""
        environment = values.get("ENVIRONMENT", "development")
        if environment == "production" and v == "dev_secret_key_change_in_production":
            raise ValueError("SECRET_KEY deve ser alterada em produção!")
        return v
    
    @property
    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento"""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_test(self) -> bool:
        """Verifica se está em ambiente de teste"""
        return self.ENVIRONMENT == "test"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instância global das configurações
settings = Settings()