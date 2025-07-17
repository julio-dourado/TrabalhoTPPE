import pytest
from sqlalchemy.orm import Session
from app.models.user import User, Gender, ActivityLevel, FitnessGoal
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService
from app.security.password import verify_password


class TestUserService:
    """Test UserService methods"""

    def test_create_user(self, db: Session):
        """Test creating a new user"""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            password="password123",
            gender=Gender.MALE,
            activity_level=ActivityLevel.MODERATE,
            main_goal=FitnessGoal.MUSCLE_GAIN,
            height_cm=180.0,
            weight_kg=80.0,
            training_experience_years=2.0,
        )
        
        user = UserService.create_user(db, user_data)
        
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.gender == Gender.MALE
        assert user.activity_level == ActivityLevel.MODERATE
        assert user.main_goal == FitnessGoal.MUSCLE_GAIN
        assert user.height_cm == 180.0
        assert user.weight_kg == 80.0
        assert user.training_experience_years == 2.0
        assert verify_password("password123", user.password_hash)
        assert user.id is not None

    def test_get_user_by_id(self, db: Session):
        """Test getting user by ID"""
        user_data = UserCreate(
            name="Jane Doe",
            email="jane@example.com",
            password="password123",
        )
        
        created_user = UserService.create_user(db, user_data)
        retrieved_user = UserService.get_user_by_id(db, created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == "Jane Doe"
        assert retrieved_user.email == "jane@example.com"

    def test_get_user_by_email(self, db: Session):
        """Test getting user by email"""
        user_data = UserCreate(
            name="Bob Smith",
            email="bob@example.com",
            password="password123",
        )
        
        created_user = UserService.create_user(db, user_data)
        retrieved_user = UserService.get_user_by_email(db, "bob@example.com")
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == "Bob Smith"
        assert retrieved_user.email == "bob@example.com"

    def test_update_user(self, db: Session):
        """Test updating user information"""
        user_data = UserCreate(
            name="Alice Johnson",
            email="alice@example.com",
            password="password123",
        )
        
        created_user = UserService.create_user(db, user_data)
        
        update_data = UserUpdate(
            name="Alice Smith",
            weight_kg=70.0,
            activity_level=ActivityLevel.INTENSE,
        )
        
        updated_user = UserService.update_user(db, created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.name == "Alice Smith"
        assert updated_user.weight_kg == 70.0
        assert updated_user.activity_level == ActivityLevel.INTENSE
        assert updated_user.email == "alice@example.com"  # Unchanged

    def test_delete_user(self, db: Session):
        """Test deleting a user"""
        user_data = UserCreate(
            name="Charlie Brown",
            email="charlie@example.com",
            password="password123",
        )
        
        created_user = UserService.create_user(db, user_data)
        user_id = created_user.id
        
        success = UserService.delete_user(db, user_id)
        assert success is True
        
        # Verify user is deleted
        retrieved_user = UserService.get_user_by_id(db, user_id)
        assert retrieved_user is None

    def test_verify_user_password(self, db: Session):
        """Test verifying user password"""
        user_data = UserCreate(
            name="Diana Prince",
            email="diana@example.com",
            password="password123",
        )
        
        created_user = UserService.create_user(db, user_data)
        
        # Test correct password
        assert UserService.verify_user_password(db, created_user.id, "password123") is True
        
        # Test incorrect password
        assert UserService.verify_user_password(db, created_user.id, "wrongpassword") is False

    def test_deactivate_user(self, db: Session):
        """Test deactivating a user"""
        user_data = UserCreate(
            name="Edward Cullen",
            email="edward@example.com",
            password="password123",
        )
        
        created_user = UserService.create_user(db, user_data)
        assert created_user.is_active == 1  # Active by default
        
        success = UserService.deactivate_user(db, created_user.id)
        assert success is True
        
        # Verify user is deactivated
        updated_user = UserService.get_user_by_id(db, created_user.id)
        assert updated_user.is_active == 0

    def test_activate_user(self, db: Session):
        """Test activating a user"""
        user_data = UserCreate(
            name="Fiona Green",
            email="fiona@example.com",
            password="password123",
        )
        
        created_user = UserService.create_user(db, user_data)
        
        # First deactivate
        UserService.deactivate_user(db, created_user.id)
        
        # Then activate
        success = UserService.activate_user(db, created_user.id)
        assert success is True
        
        # Verify user is activated
        updated_user = UserService.get_user_by_id(db, created_user.id)
        assert updated_user.is_active == 1
