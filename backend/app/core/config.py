# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: str = "test_password" 
    POSTGRES_DB: str = "test_db"
    DATABASE_URL: str = "sqlite:///./test.db"

    SECRET_KEY: str = "test_secret_key_muito_seguro_para_desenvolvimento_e_testes_123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        
settings = Settings()