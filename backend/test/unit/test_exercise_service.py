import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from datetime import datetime
from app.services import exercise_service
from app.models.exercise import Exercise, WithWeight, WithoutWeight, MuscleGroup, Difficulty, ExerciseType
from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseUpdate,
    WithWeightCreate,
    WithoutWeightCreate,
)
from app.models.training import Training


class TestExerciseService:
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)

    @pytest.fixture
    def mock_exercise_with_weight(self):
        exercise = Mock(spec=Exercise)
        exercise.id = 1
        exercise.name = "Bench Press"
        exercise.sets = 4
        exercise.reps = 8
        exercise.comment = "Test"
        exercise.exercise_type = ExerciseType.WITH_WEIGHT
        exercise.muscle_group = MuscleGroup.CHEST
        exercise.difficulty = Difficulty.BEGINNER
        exercise.rest_time_sec = 60
        exercise.is_compound = True
        exercise.equipment = "Barbell"
        exercise.instructions = "Test instructions"
        exercise.created_at = datetime.now()
        exercise.updated_at = None
        return exercise

    @pytest.fixture
    def mock_exercise_without_weight(self):
        exercise = Mock(spec=Exercise)
        exercise.id = 2
        exercise.name = "Running"
        exercise.sets = 1
        exercise.reps = 1
        exercise.comment = "Test cardio"
        exercise.exercise_type = ExerciseType.WITHOUT_WEIGHT
        exercise.muscle_group = MuscleGroup.CARDIO
        exercise.difficulty = Difficulty.BEGINNER
        exercise.rest_time_sec = 30
        exercise.is_compound = False
        exercise.equipment = "None"
        exercise.instructions = "Test cardio instructions"
        exercise.created_at = datetime.now()
        exercise.updated_at = None
        return exercise

    @pytest.fixture
    def mock_with_weight_details(self):
        with_weight = Mock(spec=WithWeight)
        with_weight.id = 1
        with_weight.exercise_id = 1
        with_weight.weight_kg = 80.0
        with_weight.max_weight_kg = 100.0
        with_weight.suggested_increment_kg = 2.5
        with_weight.created_at = datetime.now()
        with_weight.updated_at = None
        return with_weight

    @pytest.fixture
    def mock_without_weight_details(self):
        without_weight = Mock(spec=WithoutWeight)
        without_weight.id = 2
        without_weight.exercise_id = 2
        without_weight.duration_sec = 1800.0  # 30 minutes
        without_weight.distance_m = 5000.0  # 5 km
        without_weight.target_speed = 10.0  # 10 km/h
        without_weight.intensity_level = 5
        without_weight.created_at = datetime.now()
        without_weight.updated_at = None
        return without_weight

    def test_create_exercise_with_weight(self, mock_db, mock_exercise_with_weight, mock_with_weight_details):
        """Test creating an exercise with weight"""
        exercise_data = ExerciseCreate(
            name="Bench Press",
            muscle_group=MuscleGroup.CHEST,
            difficulty=Difficulty.BEGINNER,
            sets=4,
            reps=8,
            comment="Test",
            instructions="Test instructions",
            rest_time_sec=90,
            is_compound=True,
            equipment="Barbell",
            exercise_type=ExerciseType.WITH_WEIGHT,
            with_weight_details=WithWeightCreate(
                weight_kg=80.0,
                max_weight_kg=100.0,
                suggested_increment_kg=2.5,
            ),
        )

        mock_exercise_with_weight.with_weight_details = mock_with_weight_details
        mock_exercise_with_weight.without_weight_details = None

        mock_db.add.return_value = None
        mock_db.flush.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with patch('app.services.exercise_service.Exercise') as mock_exercise_class:
            mock_exercise_class.return_value = mock_exercise_with_weight
            
            with patch('app.services.exercise_service.WithWeight') as mock_with_weight_class:
                mock_with_weight_class.return_value = mock_with_weight_details
                
                result = exercise_service.create_exercise(mock_db, exercise_data)

                assert result.name == "Bench Press"
                assert result.muscle_group == MuscleGroup.CHEST
                assert result.exercise_type == ExerciseType.WITH_WEIGHT
                assert result.with_weight_details is not None
                assert result.without_weight_details is None

    def test_create_exercise_without_weight(self, mock_db, mock_exercise_without_weight, mock_without_weight_details):
        """Test creating an exercise without weight"""
        exercise_data = ExerciseCreate(
            name="Running",
            muscle_group=MuscleGroup.CARDIO,
            difficulty=Difficulty.BEGINNER,
            sets=1,
            reps=1,
            comment="Test cardio",
            instructions="Test cardio instructions",
            rest_time_sec=60,
            is_compound=False,
            equipment="None",
            exercise_type=ExerciseType.WITHOUT_WEIGHT,
            without_weight_details=WithoutWeightCreate(
                duration_sec=1800.0,
                distance_m=5000.0,
                target_speed=10.0,
                intensity_level=5,
            ),
        )

        mock_exercise_without_weight.with_weight_details = None
        mock_exercise_without_weight.without_weight_details = mock_without_weight_details

        mock_db.add.return_value = None
        mock_db.flush.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with patch('app.services.exercise_service.Exercise') as mock_exercise_class:
            mock_exercise_class.return_value = mock_exercise_without_weight
            
            with patch('app.services.exercise_service.WithoutWeight') as mock_without_weight_class:
                mock_without_weight_class.return_value = mock_without_weight_details
                
                result = exercise_service.create_exercise(mock_db, exercise_data)

                assert result.name == "Running"
                assert result.muscle_group == MuscleGroup.CARDIO
                assert result.exercise_type == ExerciseType.WITHOUT_WEIGHT
                assert result.with_weight_details is None
                assert result.without_weight_details is not None

    def test_get_all_exercises(self, mock_db, mock_exercise_with_weight, mock_with_weight_details):
        """Test getting all exercises"""
        mock_exercise_with_weight.with_weight_details = mock_with_weight_details
        mock_exercise_with_weight.without_weight_details = None

        mock_scalars = Mock()
        mock_scalars.all.return_value = [mock_exercise_with_weight]
        mock_db.scalars.return_value = mock_scalars

        result = exercise_service.get_all_exercises(mock_db)

        assert len(result) == 1
        assert result[0].name == "Bench Press"
        assert result[0].muscle_group == MuscleGroup.CHEST

    def test_get_exercise_by_id(self, mock_db, mock_exercise_with_weight, mock_with_weight_details):
        """Test getting exercise by ID"""
        mock_exercise_with_weight.with_weight_details = mock_with_weight_details
        mock_exercise_with_weight.without_weight_details = None

        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_exercise_with_weight
        mock_db.scalars.return_value = mock_scalars

        result = exercise_service.get_exercise_by_id(mock_db, 1)

        assert result is not None
        assert result.name == "Bench Press"
        assert result.id == 1

    def test_get_exercise_by_id_not_found(self, mock_db):
        """Test getting exercise by ID when not found"""
        mock_scalars = Mock()
        mock_scalars.first.return_value = None
        mock_db.scalars.return_value = mock_scalars

        result = exercise_service.get_exercise_by_id(mock_db, 999)

        assert result is None

    def test_delete_exercise(self, mock_db, mock_exercise_with_weight):
        """Test deleting an exercise"""
        mock_scalars = Mock()
        mock_scalars.first.return_value = mock_exercise_with_weight
        mock_db.scalars.return_value = mock_scalars

        mock_db.delete.return_value = None
        mock_db.commit.return_value = None

        result = exercise_service.delete_exercise(mock_db, 1)

        assert result is True
        mock_db.delete.assert_called_once_with(mock_exercise_with_weight)
        mock_db.commit.assert_called_once()

    def test_delete_exercise_not_found(self, mock_db):
        """Test deleting an exercise that doesn't exist"""
        mock_scalars = Mock()
        mock_scalars.first.return_value = None
        mock_db.scalars.return_value = mock_scalars

        result = exercise_service.delete_exercise(mock_db, 999)

        assert result is False
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()
