# app/core/security.py
import os
from typing import List
from .config import settings

def get_cors_origins() -> List[str]:
    """Get CORS origins based on environment"""
    if settings.ENVIRONMENT == "production":
        return [
            "https://yourdomain.com",
            "https://www.yourdomain.com",
            "https://api.yourdomain.com",
        ]
    else:
        return settings.CORS_ORIGINS

def get_secret_key() -> str:
    """Get secret key from environment or raise error in production"""
    secret_key = os.getenv("SECRET_KEY", settings.SECRET_KEY)
    
    if settings.ENVIRONMENT == "production":
        if secret_key == "your-secret-key-here-change-in-production":
            raise ValueError("SECRET_KEY must be set in production environment")
        if len(secret_key) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
    
    return secret_key

def get_database_url() -> str:
    """Get database URL with validation"""
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    
    if settings.ENVIRONMENT == "production":
        if "sqlite" in db_url:
            raise ValueError("SQLite is not recommended for production")
        if "postgresql" not in db_url:
            raise ValueError("PostgreSQL is recommended for production")
    
    return db_url

# Security headers para produção
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
} 