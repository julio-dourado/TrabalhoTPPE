# app/core/config.py
from typing import List, Union
from pydantic import validator
from pydantic_settings import BaseSettings as PydanticBaseSettings


class Settings(PydanticBaseSettings):
    """Application settings configuration"""

    # Database configuration
    DATABASE_URL: str = "sqlite:///./workout_app.db"
    DATABASE_URL_TEST: str = "sqlite:///./test_workout_app.db"

    # JWT configuration
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Workout API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A FastAPI application for workout management"

    # Security configuration
    BCRYPT_ROUNDS: int = 12

    # Pagination configuration
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # File upload configuration
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"

    # Email configuration (for future use)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "noreply@workoutapp.com"
    EMAILS_FROM_NAME: str = "Workout App"

    # Redis configuration (for future use)
    REDIS_URL: str = "redis://localhost:6379"

    # Logging configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global settings instance
settings = Settings()

# Database configuration for SQLAlchemy
DATABASE_CONFIG = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "connect_args": {
        "check_same_thread": False,
    },
}

# JWT configuration
JWT_CONFIG = {
    "secret_key": settings.SECRET_KEY,
    "algorithm": settings.ALGORITHM,
    "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
}

# CORS configuration
CORS_CONFIG = {
    "allow_origins": settings.CORS_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
