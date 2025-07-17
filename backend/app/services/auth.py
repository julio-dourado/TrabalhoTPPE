from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenData
from app.schemas.user import UserOut
from app.security.password import verify_password, get_password_hash
from app.security.jwt import create_access_token, verify_token


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        stmt = select(User).where(User.email == email)
        user = db.scalars(stmt).first()
        
        if not user:
            return None
            
        if not verify_password(password, user.password_hash):
            return None
            
        return user

    @staticmethod
    def create_user(db: Session, user_data: RegisterRequest) -> User:
        """Create a new user"""
        password_hash = get_password_hash(user_data.password)
        
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=password_hash,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        stmt = select(User).where(User.id == user_id)
        return db.scalars(stmt).first()

    @staticmethod
    def login_user(db: Session, login_data: LoginRequest) -> dict:
        """Login user and return token"""
        user = AuthService.authenticate_user(db, login_data.email, login_data.password)
        
        if not user:
            raise ValueError("Invalid credentials")
        
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,  # 30 minutes
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
                "is_premium": user.is_premium,
            }
        }

    @staticmethod
    def register_user(db: Session, register_data: RegisterRequest) -> dict:
        """Register a new user"""
        # Check if user already exists
        existing_user = AuthService.get_user_by_email(db, register_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Validate password confirmation
        if register_data.password != register_data.confirm_password:
            raise ValueError("Passwords do not match")
        
        # Create user
        user = AuthService.create_user(db, register_data)
        
        return {
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
                "is_premium": user.is_premium,
            }
        }

    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        """Get current user from token"""
        try:
            payload = verify_token(token)
            user_id = payload.get("sub")
            
            if user_id is None:
                raise ValueError("Invalid token")
            
            user = AuthService.get_user_by_id(db, int(user_id))
            
            if user is None:
                raise ValueError("User not found")
            
            return user
            
        except Exception as e:
            raise ValueError(f"Token validation failed: {str(e)}")
