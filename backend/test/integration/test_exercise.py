import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.models.exercise import (
    Exercise,
    WithWeight,
    WithoutWeight,
    MuscleGroup,
    Difficulty,
    ExerciseType,
)
from app.models.training import Training
from app.services import exercise_service

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


class TestExerciseRoutes:
    """Tests for exercise routes"""

    def test_create_exercise_with_weight_success(self, client_with_db: TestClient):
        """
        US11: Test creating exercise with weight
        """
        # Get auth token
        token = create_authenticated_user(client_with_db)
        headers = {"Authorization": f"Bearer {token}"}

        exercise_data = {
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

        response = client_with_db.post("/api/v1/exercises/", json=exercise_data, headers=headers)

        assert response.status_code == 201
        data = response.json()
        
        assert data["name"] == "Bench Press"
        assert data["muscle_group"] == "PEITO"
        assert data["difficulty"] == "INICIANTE"
        assert data["sets"] == 4
        assert data["reps"] == 8
        assert data["comment"] == "Focus on chest"
        assert data["instructions"] == "Lie on bench, grip bar with medium grip"
        assert data["rest_time_sec"] == 90
        assert data["is_compound"] == True
        assert data["equipment"] == "Olympic barbell"
        assert data["exercise_type"] == "COM_PESO"
        assert data["with_weight_details"]["weight_kg"] == 80.0
        assert data["with_weight_details"]["max_weight_kg"] == 100.0
        assert data["with_weight_details"]["suggested_increment_kg"] == 2.5
        assert data["without_weight_details"] is None
        assert "id" in data

    def test_create_exercise_without_weight_success(self, client_with_db: TestClient):
        """
        US11: Test creating exercise without weight
        """
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test2@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        exercise_data = {
            "name": "Running",
            "muscle_group": "CARDIO",
            "difficulty": "INICIANTE",
            "sets": 1,
            "reps": 1,
            "comment": "Cardio exercise",
            "instructions": "Run at steady pace",
            "rest_time_sec": 60,
            "is_compound": False,
            "equipment": "None",
            "exercise_type": "SEM_PESO",
            "without_weight_details": {
                "duration_sec": 1800.0,
                "distance_m": 5000.0,
                "target_speed": 10.0,
                "intensity_level": 5,
            },
        }

        response = client_with_db.post("/api/v1/exercises/", json=exercise_data, headers=headers)

        assert response.status_code == 201
        data = response.json()
        
        assert data["name"] == "Running"
        assert data["muscle_group"] == "CARDIO"
        assert data["difficulty"] == "INICIANTE"
        assert data["sets"] == 1
        assert data["reps"] == 1
        assert data["comment"] == "Cardio exercise"
        assert data["instructions"] == "Run at steady pace"
        assert data["rest_time_sec"] == 60
        assert data["is_compound"] == False
        assert data["equipment"] == "None"
        assert data["exercise_type"] == "SEM_PESO"
        assert data["without_weight_details"]["duration_sec"] == 1800.0
        assert data["without_weight_details"]["distance_m"] == 5000.0
        assert data["without_weight_details"]["target_speed"] == 10.0
        assert data["without_weight_details"]["intensity_level"] == 5
        assert data["with_weight_details"] is None
        assert "id" in data

    def test_create_exercise_with_weight_validation_errors(self, client_with_db: TestClient):
        """Test creating exercise with validation errors"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test3@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        exercise_data = {
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
            # Missing with_weight_details
        }

        response = client_with_db.post("/api/v1/exercises/", json=exercise_data, headers=headers)

        assert response.status_code == 422  # Validation error

    def test_create_exercise_without_weight_validation_errors(self, client_with_db: TestClient):
        """Test creating exercise without weight with validation errors"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test4@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        exercise_data = {
            "name": "Running",
            "muscle_group": "CARDIO",
            "difficulty": "INICIANTE",
            "sets": 1,
            "reps": 1,
            "comment": "Cardio exercise",
            "instructions": "Run at steady pace",
            "rest_time_sec": 60,
            "is_compound": False,
            "equipment": "None",
            "exercise_type": "SEM_PESO",
            # Missing without_weight_details
        }

        response = client_with_db.post("/api/v1/exercises/", json=exercise_data, headers=headers)

        assert response.status_code == 422  # Validation error

    def test_get_all_exercises(self, client_with_db: TestClient):
        """Test getting all exercises"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test5@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # First create some exercises
        exercise_data_1 = {
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
        
        exercise_data_2 = {
            "name": "Running",
            "muscle_group": "CARDIO",
            "difficulty": "INICIANTE",
            "sets": 1,
            "reps": 1,
            "comment": "Cardio exercise",
            "instructions": "Run at steady pace",
            "rest_time_sec": 60,
            "is_compound": False,
            "equipment": "None",
            "exercise_type": "SEM_PESO",
            "without_weight_details": {
                "duration_sec": 1800.0,
                "distance_m": 5000.0,
                "target_speed": 10.0,
                "intensity_level": 5,
            },
        }

        # Create exercises
        response1 = client_with_db.post("/api/v1/exercises/", json=exercise_data_1, headers=headers)
        response2 = client_with_db.post("/api/v1/exercises/", json=exercise_data_2, headers=headers)
        
        assert response1.status_code == 201
        assert response2.status_code == 201

        # Get all exercises
        response = client_with_db.get("/api/v1/exercises/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Bench Press"
        assert data[1]["name"] == "Running"

    def test_get_exercise_by_id(self, client_with_db: TestClient):
        """Test getting exercise by ID"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test6@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create an exercise first
        exercise_data = {
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

        create_response = client_with_db.post("/api/v1/exercises/", json=exercise_data, headers=headers)
        assert create_response.status_code == 201
        created_exercise = create_response.json()

        # Get the exercise by ID
        response = client_with_db.get(f"/api/v1/exercises/{created_exercise['id']}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_exercise["id"]
        assert data["name"] == "Bench Press"
        assert data["muscle_group"] == "PEITO"

    def test_get_exercise_by_id_not_found(self, client_with_db: TestClient):
        """Test getting exercise by ID that doesn't exist"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test7@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = client_with_db.get("/api/v1/exercises/999", headers=headers)
        
        assert response.status_code == 404

    def test_update_exercise(self, client_with_db: TestClient):
        """Test updating an exercise"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test8@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create an exercise first
        exercise_data = {
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

        create_response = client_with_db.post("/api/v1/exercises/", json=exercise_data, headers=headers)
        assert create_response.status_code == 201
        created_exercise = create_response.json()

        # Update the exercise
        update_data = {
            "name": "Incline Bench Press",
            "sets": 5,
            "reps": 6,
            "with_weight_details": {
                "weight_kg": 90.0,
                "max_weight_kg": 110.0,
                "suggested_increment_kg": 5.0,
            },
        }

        response = client_with_db.put(f"/api/v1/exercises/{created_exercise['id']}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Incline Bench Press"
        assert data["sets"] == 5
        assert data["reps"] == 6
        assert data["with_weight_details"]["weight_kg"] == 90.0

    def test_update_exercise_not_found(self, client_with_db: TestClient):
        """Test updating exercise that doesn't exist"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test9@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        update_data = {
            "name": "Updated Exercise",
            "sets": 5,
        }

        response = client_with_db.put("/api/v1/exercises/999", json=update_data, headers=headers)
        
        assert response.status_code == 404

    def test_delete_exercise(self, client_with_db: TestClient):
        """Test deleting an exercise"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test10@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create an exercise first
        exercise_data = {
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

        create_response = client_with_db.post("/api/v1/exercises/", json=exercise_data, headers=headers)
        assert create_response.status_code == 201
        created_exercise = create_response.json()

        # Delete the exercise
        response = client_with_db.delete(f"/api/v1/exercises/{created_exercise['id']}", headers=headers)
        
        assert response.status_code == 204

        # Verify it's deleted
        get_response = client_with_db.get(f"/api/v1/exercises/{created_exercise['id']}", headers=headers)
        assert get_response.status_code == 404

    def test_delete_exercise_not_found(self, client_with_db: TestClient):
        """Test deleting exercise that doesn't exist"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test11@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        response = client_with_db.delete("/api/v1/exercises/999", headers=headers)
        
        assert response.status_code == 404

    def test_get_exercises_by_muscle_group(self, client_with_db: TestClient):
        """Test getting exercises by muscle group"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test12@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create exercises with different muscle groups
        exercise_data_1 = {
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
        
        exercise_data_2 = {
            "name": "Squat",
            "muscle_group": "PERNAS",
            "difficulty": "INICIANTE",
            "sets": 4,
            "reps": 8,
            "comment": "Focus on legs",
            "instructions": "Keep feet shoulder-width apart",
            "rest_time_sec": 90,
            "is_compound": True,
            "equipment": "Olympic barbell",
            "exercise_type": "COM_PESO",
            "with_weight_details": {
                "weight_kg": 100.0,
                "max_weight_kg": 120.0,
                "suggested_increment_kg": 5.0,
            },
        }

        # Create exercises
        client_with_db.post("/api/v1/exercises/", json=exercise_data_1, headers=headers)
        client_with_db.post("/api/v1/exercises/", json=exercise_data_2, headers=headers)

        # Get exercises by muscle group
        response = client_with_db.get("/api/v1/exercises/muscle-group/PEITO", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Bench Press"
        assert data[0]["muscle_group"] == "PEITO"

    def test_get_exercises_by_difficulty(self, client_with_db: TestClient):
        """Test getting exercises by difficulty"""
        # Get auth token
        token = create_authenticated_user(client_with_db, email="test13@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create exercises with different difficulties
        exercise_data_1 = {
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
        
        exercise_data_2 = {
            "name": "Deadlift",
            "muscle_group": "COSTAS",
            "difficulty": "AVANCADO",
            "sets": 3,
            "reps": 5,
            "comment": "Complex movement",
            "instructions": "Keep back straight, lift with legs",
            "rest_time_sec": 120,
            "is_compound": True,
            "equipment": "Olympic barbell",
            "exercise_type": "COM_PESO",
            "with_weight_details": {
                "weight_kg": 120.0,
                "max_weight_kg": 140.0,
                "suggested_increment_kg": 5.0,
            },
        }

        # Create exercises
        client_with_db.post("/api/v1/exercises/", json=exercise_data_1, headers=headers)
        client_with_db.post("/api/v1/exercises/", json=exercise_data_2, headers=headers)

        # Get exercises by difficulty
        response = client_with_db.get("/api/v1/exercises/difficulty/INICIANTE", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Bench Press"
        assert data[0]["difficulty"] == "INICIANTE"
