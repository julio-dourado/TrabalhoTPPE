import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.security.password import verify_password, get_password_hash
from app.core.config import settings
from app.security.jwt import create_access_token, decode_token
from app.schemas.training import TrainingCreate
from app.schemas.exercise import ExerciseCreate, WithWeightCreate, WithoutWeightCreate
from app.models.exercise import MuscleGroup, Difficulty, ExerciseType
from app.models.training import TrainingCategory, TrainingStatus

# Note: As fixtures 'client_with_db' e 'db' são importadas
# automaticamente de conftest.py pelo pytest.


def create_authenticated_user(client: TestClient, email: str = "test@example.com", name: str = "Test User") -> str:
    """Helper function to create a user and return auth token"""
    user_data = {
        "name": name,
        "email": email,
        "password": "password123",
    }
    client.post("/api/v1/users/", json=user_data)
    
    response_login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "password123"},
    )
    return response_login.json()["access_token"]


class TestTrainingIntegration:
    """Integration tests for training functionality"""

    def test_create_training_success(self, client_with_db: TestClient, db: Session):
        """Test creating a training successfully"""
        # Create user and login
        token = create_authenticated_user(client_with_db)
        headers = {"Authorization": f"Bearer {token}"}

        # Create training with complete exercise
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }

        response = client_with_db.post("/api/v1/training/", json=training_data, headers=headers)
        
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "Push Training"
        assert data["description"] == "Push exercises for chest, shoulders, and triceps"
        assert data["category"] == "FORCA"
        assert data["estimated_duration_min"] == 60
        assert data["status"] == "PLANEJADO"
        assert "id" in data
        assert len(data["exercises"]) == 1
        assert data["exercises"][0]["name"] == "Bench Press"

    def test_create_training_with_exercises(self, client_with_db: TestClient, db: Session):
        """Test creating a training with exercises"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test2@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create training with multiple exercises
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                },
                {
                    "name": "Push-ups",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 3,
                    "reps": 15,
                    "comment": "Bodyweight chest exercise",
                    "instructions": "Keep body straight, push up from ground",
                    "rest_time_sec": 60,
                    "is_compound": True,
                    "equipment": "None",
                    "exercise_type": "SEM_PESO",
                    "without_weight_details": {
                        "duration_sec": 900.0,
                        "distance_m": 1000.0,
                        "target_speed": 5.0,
                        "intensity_level": 3,
                    },
                },
            ],
        }

        response = client_with_db.post("/api/v1/training/", json=training_data, headers=headers)
        
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "Push Training"
        assert len(data["exercises"]) == 2
        assert data["exercises"][0]["name"] == "Bench Press"
        assert data["exercises"][1]["name"] == "Push-ups"

    def test_get_training_by_id(self, client_with_db: TestClient, db: Session):
        """Test getting a training by ID"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test3@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create training
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }

        create_response = client_with_db.post("/api/v1/training/", json=training_data, headers=headers)
        assert create_response.status_code == 201
        training_id = create_response.json()["id"]

        # Get training
        response = client_with_db.get(f"/api/v1/training/{training_id}", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == training_id
        assert data["name"] == "Push Training"
        assert data["description"] == "Push exercises for chest, shoulders, and triceps"

    def test_get_training_not_found(self, client_with_db: TestClient, db: Session):
        """Test getting a training that doesn't exist"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test4@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = client_with_db.get("/api/v1/training/999", headers=headers)
        assert response.status_code == 404

    def test_get_all_trainings(self, client_with_db: TestClient, db: Session):
        """Test getting all trainings"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test5@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create trainings
        training_data_1 = {
            "name": "Push Training",
            "description": "Push exercises",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }
        
        training_data_2 = {
            "name": "Pull Training",
            "description": "Pull exercises",
            "category": "FORCA",
            "estimated_duration_min": 45,
            "exercises": [
                {
                    "name": "Deadlift",
                    "muscle_group": "PEITO",
                    "difficulty": "INTERMEDIARIO",
                    "sets": 3,
                    "reps": 8,
                    "comment": "Focus on back",
                    "instructions": "Stand with barbell, bend at hips, pull up",
                    "rest_time_sec": 120,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 120.0,
                        "max_weight_kg": 150.0,
                        "suggested_increment_kg": 5.0,
                    },
                }
            ],
        }

        client_with_db.post("/api/v1/training/", json=training_data_1, headers=headers)
        client_with_db.post("/api/v1/training/", json=training_data_2, headers=headers)

        # Get all trainings
        response = client_with_db.get("/api/v1/training/", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Push Training"
        assert data[1]["name"] == "Pull Training"

    def test_update_training(self, client_with_db: TestClient, db: Session):
        """Test updating a training"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test6@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create training
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }

        create_response = client_with_db.post("/api/v1/training/", json=training_data, headers=headers)
        assert create_response.status_code == 201
        training_id = create_response.json()["id"]

        # Update training
        update_data = {
            "name": "Updated Push Training",
            "description": "Updated description",
            "estimated_duration_min": 90,
        }
        
        response = client_with_db.put(f"/api/v1/training/{training_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated Push Training"
        assert data["description"] == "Updated description"
        assert data["estimated_duration_min"] == 90

    def test_update_training_not_found(self, client_with_db: TestClient, db: Session):
        """Test updating a training that doesn't exist"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test7@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        update_data = {
            "name": "Updated Training",
            "description": "Updated description",
        }
        
        response = client_with_db.put("/api/v1/training/999", json=update_data, headers=headers)
        assert response.status_code == 404

    def test_delete_training(self, client_with_db: TestClient, db: Session):
        """Test deleting a training"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test8@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create training
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }

        create_response = client_with_db.post("/api/v1/training/", json=training_data, headers=headers)
        assert create_response.status_code == 201
        training_id = create_response.json()["id"]

        # Delete training
        response = client_with_db.delete(f"/api/v1/training/{training_id}", headers=headers)
        assert response.status_code == 204

        # Verify training is deleted
        get_response = client_with_db.get(f"/api/v1/training/{training_id}", headers=headers)
        assert get_response.status_code == 404

    def test_delete_training_not_found(self, client_with_db: TestClient, db: Session):
        """Test deleting a training that doesn't exist"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test9@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = client_with_db.delete("/api/v1/training/999", headers=headers)
        assert response.status_code == 404

    def test_training_unauthorized(self, client_with_db: TestClient, db: Session):
        """Test accessing training endpoints without authentication"""
        # Test creating training without auth
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }

        response = client_with_db.post("/api/v1/training/", json=training_data)
        assert response.status_code == 403

        # Test getting training without auth
        response = client_with_db.get("/api/v1/training/")
        assert response.status_code == 403

        # Test getting training by ID without auth
        response = client_with_db.get("/api/v1/training/1")
        assert response.status_code == 403

        # Test updating training without auth
        response = client_with_db.put("/api/v1/training/1", json={"name": "Updated"})
        assert response.status_code == 403

        # Test deleting training without auth
        response = client_with_db.delete("/api/v1/training/1")
        assert response.status_code == 403

    def test_start_training_session(self, client_with_db: TestClient, db: Session):
        """Test starting a training session"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test12@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create training
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }

        create_response = client_with_db.post("/api/v1/training/", json=training_data, headers=headers)
        assert create_response.status_code == 201
        training_id = create_response.json()["id"]

        # Start training session
        response = client_with_db.post(f"/api/v1/training/{training_id}/start", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "EM_ANDAMENTO"
        assert "started_at" in data

    def test_finish_training_session(self, client_with_db: TestClient, db: Session):
        """Test finishing a training session"""
        # Create user and login
        token = create_authenticated_user(client_with_db, email="test13@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create training
        training_data = {
            "name": "Push Training",
            "description": "Push exercises for chest, shoulders, and triceps",
            "category": "FORCA",
            "estimated_duration_min": 60,
            "exercises": [
                {
                    "name": "Bench Press",
                    "muscle_group": "PEITO",
                    "difficulty": "INICIANTE",
                    "sets": 4,
                    "reps": 8,
                    "comment": "Focus on chest",
                    "instructions": "Lie on bench, grip bar with medium grip",
                    "rest_time_sec": 90,
                    "is_compound": True,
                    "equipment": "Olympic barbell",
                    "exercise_type": "COM_PESO",
                    "with_weight_details": {
                        "weight_kg": 80.0,
                        "max_weight_kg": 100.0,
                        "suggested_increment_kg": 2.5,
                    },
                }
            ],
        }

        create_response = client_with_db.post("/api/v1/training/", json=training_data, headers=headers)
        assert create_response.status_code == 201
        training_id = create_response.json()["id"]

        # Start training session
        start_response = client_with_db.post(f"/api/v1/training/{training_id}/start", headers=headers)
        assert start_response.status_code == 200

        # Finish training session
        finish_data = {
            "status": "CONCLUIDO",
            "actual_duration_min": 65,
            "calories_burned": 300.0,
            "perceived_difficulty": 7,
            "satisfaction": 4,
            "observations": "Good workout"
        }
        
        response = client_with_db.post(f"/api/v1/training/{training_id}/finish", json=finish_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "CONCLUIDO"
        assert "finished_at" in data
