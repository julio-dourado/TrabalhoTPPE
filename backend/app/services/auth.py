# app/services/auth.py
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.security.password import verify_password, get_password_hash


# Authentication service functions


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
    """Update user password"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return True


def deactivate_user(db: Session, user_id: int) -> bool:
    """Deactivate user account"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.is_active = False
    db.commit()
    return True


def activate_user(db: Session, user_id: int) -> bool:
    """Activate user account"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.is_active = True
    db.commit()
    return True


def check_user_exists(db: Session, email: str) -> bool:
    """Check if user exists by email"""
    return get_user_by_email(db, email) is not None


def verify_user_password(db: Session, user_id: int, password: str) -> bool:
    """Verify user password"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    return verify_password(password, user.hashed_password)


def get_active_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get active user by ID"""
    return db.query(User).filter(
        User.id == user_id, User.is_active is True
    ).first()


def get_active_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get active user by email"""
    return db.query(User).filter(
        User.email == email, User.is_active is True
    ).first()
