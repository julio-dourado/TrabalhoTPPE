# app/core/config.py
import os
from typing import Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Training API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", description="Runtime environment")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # Database configuration
    POSTGRES_USER: str = Field(default="test_user", description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(
        default="test_password", description="PostgreSQL password"
    )
    POSTGRES_DB: str = Field(default="test_db", description="PostgreSQL database name")
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")

    # Database URL (automatically calculated)
    DATABASE_URL: Optional[str] = None

    # Security configuration
    SECRET_KEY: str = Field(
        default="dev_secret_key_change_in_production",
        min_length=32,
        description="Secret key for JWT",
    )
    ALGORITHM: str = Field(default="HS256", description="Encryption algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        ge=1,
        le=10080,  # maximum 1 week
        description="Token expiration time in minutes",
    )

    # CORS configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed origins for CORS",
    )

    # Logging configuration
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format",
    )

    # File configuration
    UPLOAD_DIR: str = Field(default="uploads", description="Upload directory")
    MAX_FILE_SIZE: int = Field(
        default=10_000_000, description="Maximum file size in bytes"
    )

    @validator("DATABASE_URL", pre=True, always=True)
    def build_database_url(cls, v, values):
        if v:
            return v

        environment = values.get("ENVIRONMENT", "development")

        if environment == "test":
            return "sqlite:///./test.db"
        elif environment == "development":
            return "sqlite:///./development.db"
        else:
            # Production uses PostgreSQL
            user = values.get("POSTGRES_USER")
            password = values.get("POSTGRES_PASSWORD")
            host = values.get("POSTGRES_HOST")
            port = values.get("POSTGRES_PORT")
            db = values.get("POSTGRES_DB")
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate if the environment is valid"""
        allowed_envs = ["development", "test", "staging", "production"]
        if v not in allowed_envs:
            raise ValueError(f"Environment must be one of: {allowed_envs}")
        return v

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v, values):
        """Validate the secret key in production"""
        environment = values.get("ENVIRONMENT", "development")
        if environment == "production" and v == "dev_secret_key_change_in_production":
            raise ValueError("SECRET_KEY must be changed in production!")
        return v

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_test(self) -> bool:
        return self.ENVIRONMENT == "test"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
