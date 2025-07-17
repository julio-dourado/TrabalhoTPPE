from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.security.password import get_password_hash, verify_password


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        password_hash = get_password_hash(user_data.password)
        
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=password_hash,
            birth_date=user_data.birth_date,
            gender=user_data.gender,
            height_cm=user_data.height_cm,
            weight_kg=user_data.weight_kg,
            activity_level=user_data.activity_level,
            main_goal=user_data.main_goal,
            training_experience_years=user_data.training_experience_years,
            bio=user_data.bio,
            target_weight_kg=user_data.target_weight_kg,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        stmt = select(User).where(User.id == user_id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        stmt = select(User).offset(skip).limit(limit)
        return db.scalars(stmt).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        user = UserService.get_user_by_id(db, user_id)
        
        if not user:
            return None
        
        # Update fields if provided
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.password is not None:
            user.password_hash = get_password_hash(user_data.password)
        if user_data.birth_date is not None:
            user.birth_date = user_data.birth_date
        if user_data.gender is not None:
            user.gender = user_data.gender
        if user_data.height_cm is not None:
            user.height_cm = user_data.height_cm
        if user_data.weight_kg is not None:
            user.weight_kg = user_data.weight_kg
        if user_data.activity_level is not None:
            user.activity_level = user_data.activity_level
        if user_data.main_goal is not None:
            user.main_goal = user_data.main_goal
        if user_data.training_experience_years is not None:
            user.training_experience_years = user_data.training_experience_years
        if user_data.bio is not None:
            user.bio = user_data.bio
        if user_data.target_weight_kg is not None:
            user.target_weight_kg = user_data.target_weight_kg
        
        user.updated_at = datetime.now()
        
        db.commit()
        db.refresh(user)
        
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user"""
        user = UserService.get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        
        return True

    @staticmethod
    def verify_user_password(db: Session, user_id: int, password: str) -> bool:
        """Verify user password"""
        user = UserService.get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        return verify_password(password, user.password_hash)

    @staticmethod
    def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
        """Update user password"""
        user = UserService.get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        user.password_hash = get_password_hash(new_password)
        user.updated_at = datetime.now()
        
        db.commit()
        db.refresh(user)
        
        return True

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> bool:
        """Deactivate a user"""
        user = UserService.get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.now()
        
        db.commit()
        db.refresh(user)
        
        return True

    @staticmethod
    def activate_user(db: Session, user_id: int) -> bool:
        """Activate a user"""
        user = UserService.get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        user.is_active = True
        user.updated_at = datetime.now()
        
        db.commit()
        db.refresh(user)
        
        return True
