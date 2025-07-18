import pytest
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session
from app.services import training_service
from app.models.training import Training, TrainingStatus, TrainingCategory
from app.models.exercise import Exercise, WithWeight, WithoutWeight, MuscleGroup, Difficulty, ExerciseType
from app.models.user import User
from app.schemas.training import TrainingCreate, TrainingCreateWithExercises, TrainingUpdate, TrainingFilters
from app.schemas.exercise import ExerciseCreate, WithWeightCreate, WithoutWeightCreate
from datetime import datetime


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def sample_user():
    user = Mock(spec=User)
    user.id = 1
    user.name = "Test User"
    user.email = "test@example.com"
    return user


@pytest.fixture
def sample_training_create():
    return TrainingCreateWithExercises(
        name="Test Training",
        description="Test training description",
        category=TrainingCategory.STRENGTH,
        estimated_duration_min=60,
        exercises=[
            ExerciseCreate(
                name="Bench Press",
                sets=3,
                reps=10,
                comment="Test exercise",
                instructions="Lie on bench and push bar",
                equipment="Barbell",
                exercise_type=ExerciseType.WITH_WEIGHT,
                muscle_group=MuscleGroup.CHEST,
                difficulty=Difficulty.INTERMEDIATE,
                rest_time_sec=90,
                is_compound=True,
                with_weight_details=WithWeightCreate(
                    weight_kg=80.0,
                    max_weight_kg=100.0,
                    suggested_increment_kg=2.5,
                ),
            ),
            ExerciseCreate(
                name="Running",
                sets=1,
                reps=1,
                comment="Cardio exercise",
                instructions="Run at steady pace",
                equipment="None",
                exercise_type=ExerciseType.WITHOUT_WEIGHT,
                muscle_group=MuscleGroup.CARDIO,
                difficulty=Difficulty.BEGINNER,
                rest_time_sec=60,
                is_compound=False,
                without_weight_details=WithoutWeightCreate(
                    duration_sec=1800.0,
                    distance_m=5000.0,
                    target_speed=10.0,
                    intensity_level=5,
                ),
            ),
        ],
    )


@pytest.fixture
def sample_training_update():
    return TrainingUpdate(
        name="Updated Training",
        description="Updated description",
        status=TrainingStatus.COMPLETED,
        actual_duration_min=75,
        calories_burned=450.0,
        total_volume_kg=2400.0,
        perceived_difficulty=7,
        satisfaction=4,
        observations="Good training session",
    )


@pytest.fixture
def mock_training():
    training = Mock(spec=Training)
    training.id = 1
    training.name = "Test Training"
    training.description = "Test training description"
    training.category = TrainingCategory.STRENGTH
    training.user_id = 1
    training.status = TrainingStatus.PLANNED
    training.estimated_duration_min = 60
    training.actual_duration_min = None
    training.calories_burned = None
    training.total_volume_kg = None
    training.perceived_difficulty = None
    training.satisfaction = None
    training.observations = None
    training.created_at = datetime.now()
    training.updated_at = None
    training.started_at = None
    training.finished_at = None
    training.exercises = []
    return training


@pytest.fixture
def mock_exercise_with_weight():
    exercise = Mock(spec=Exercise)
    exercise.id = 1
    exercise.name = "Bench Press"
    exercise.sets = 3
    exercise.reps = 10
    exercise.comment = "Test exercise"
    exercise.instructions = "Lie on bench and push bar"
    exercise.equipment = "Barbell"
    exercise.exercise_type = ExerciseType.WITH_WEIGHT
    exercise.muscle_group = MuscleGroup.CHEST
    exercise.difficulty = Difficulty.INTERMEDIATE
    exercise.rest_time_sec = 90
    exercise.is_compound = True
    exercise.created_at = datetime.now()
    exercise.updated_at = None
    
    with_weight = Mock(spec=WithWeight)
    with_weight.id = 1
    with_weight.exercise_id = 1
    with_weight.weight_kg = 80.0
    with_weight.max_weight_kg = 100.0
    with_weight.suggested_increment_kg = 2.5
    with_weight.created_at = datetime.now()
    with_weight.updated_at = None
    
    exercise.with_weight_details = with_weight
    exercise.without_weight_details = None
    
    return exercise


@pytest.fixture
def mock_exercise_without_weight():
    exercise = Mock(spec=Exercise)
    exercise.id = 2
    exercise.name = "Running"
    exercise.sets = 1
    exercise.reps = 1
    exercise.comment = "Cardio exercise"
    exercise.instructions = "Run at steady pace"
    exercise.equipment = "None"
    exercise.exercise_type = ExerciseType.WITHOUT_WEIGHT
    exercise.muscle_group = MuscleGroup.CARDIO
    exercise.difficulty = Difficulty.BEGINNER
    exercise.rest_time_sec = 60
    exercise.is_compound = False
    exercise.created_at = datetime.now()
    exercise.updated_at = None
    
    without_weight = Mock(spec=WithoutWeight)
    without_weight.id = 2
    without_weight.exercise_id = 2
    without_weight.duration_sec = 1800.0
    without_weight.distance_m = 5000.0
    without_weight.target_speed = 10.0
    without_weight.intensity_level = 5
    without_weight.created_at = datetime.now()
    without_weight.updated_at = None
    
    exercise.with_weight_details = None
    exercise.without_weight_details = without_weight
    
    return exercise


class TestTrainingService:
    
    def test_create_training_success(self, mock_db, sample_training_create, mock_training, mock_exercise_with_weight, mock_exercise_without_weight):
        """Test creating a training successfully"""
        mock_training.exercises = [mock_exercise_with_weight, mock_exercise_without_weight]
        
        mock_db.add.return_value = None
        mock_db.flush.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        with patch('app.services.training_service.Training') as mock_training_class:
            mock_training_class.return_value = mock_training
            
            with patch('app.services.training_service.create_exercise') as mock_create_exercise:
                # Mock the create_exercise function to return exercise schemas
                from app.schemas.exercise import ExerciseOut, WithWeightOut
                exercise_out_1 = ExerciseOut(
                    id=1,
                    name="Bench Press",
                    sets=3,
                    reps=10,
                    comment="Test exercise",
                    instructions="Lie on bench and push bar",
                    equipment="Barbell",
                    exercise_type=ExerciseType.WITH_WEIGHT,
                    muscle_group=MuscleGroup.CHEST,
                    difficulty=Difficulty.INTERMEDIATE,
                    rest_time_sec=90,
                    is_compound=True,
                    created_at=datetime.now(),
                    updated_at=None,
                    with_weight_details=WithWeightOut(
                        id=1,
                        exercise_id=1,
                        weight_kg=80.0,
                        max_weight_kg=100.0,
                        suggested_increment_kg=2.5,
                        created_at=datetime.now(),
                        updated_at=None
                    ),
                    without_weight_details=None
                )
                
                exercise_out_2 = ExerciseOut(
                    id=2,
                    name="Running",
                    sets=1,
                    reps=1,
                    comment="Cardio exercise",
                    instructions="Run at steady pace",
                    equipment="None",
                    exercise_type=ExerciseType.WITHOUT_WEIGHT,
                    muscle_group=MuscleGroup.CARDIO,
                    difficulty=Difficulty.BEGINNER,
                    rest_time_sec=60,
                    is_compound=False,
                    created_at=datetime.now(),
                    updated_at=None,
                    with_weight_details=None,
                    without_weight_details=None  # Simplified for this test
                )
                
                mock_create_exercise.side_effect = [exercise_out_1, exercise_out_2]
                
                # Mock the query to return the exercises
                mock_query = Mock()
                mock_query.filter.return_value.first.side_effect = [mock_exercise_with_weight, mock_exercise_without_weight]
                mock_db.query.return_value = mock_query
                
                result = training_service.create_training_with_exercises(mock_db, sample_training_create, 1)
                
                assert result.name == "Test Training"
                assert result.user_id == 1
                assert result.category == TrainingCategory.STRENGTH
                assert len(result.exercises) == 4
                assert mock_db.add.called
                assert mock_db.commit.called

    def test_get_training_by_id_found(self, mock_db, mock_training, mock_exercise_with_weight):
        """Test getting training by ID when found"""
        mock_training.exercises = [mock_exercise_with_weight]
        
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_training
        mock_db.query.return_value = mock_query
        
        result = training_service.get_training_by_id(mock_db, 1)
        
        assert result is not None
        assert result.id == 1
        assert result.name == "Test Training"
        assert len(result.exercises) == 1

    def test_get_training_by_id_not_found(self, mock_db):
        """Test getting training by ID when not found"""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query
        
        result = training_service.get_training_by_id(mock_db, 999)
        
        assert result is None

    def test_get_user_trainings(self, mock_db, mock_training, mock_exercise_with_weight):
        """Test getting user trainings"""
        mock_training.exercises = [mock_exercise_with_weight]
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [mock_training]
        mock_db.query.return_value = mock_query
        
        filters = TrainingFilters(user_id=1)
        result = training_service.get_user_trainings(mock_db, filters)
        
        assert len(result) == 1
        assert result[0].name == "Test Training"
        assert result[0].user_id == 1

    def test_update_training_success(self, mock_db, sample_training_update, mock_training, mock_exercise_with_weight):
        """Test updating a training successfully"""
        mock_training.exercises = [mock_exercise_with_weight]
        
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_training
        mock_db.query.return_value = mock_query
        
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        result = training_service.update_training(mock_db, 1, sample_training_update)
        
        assert result is not None
        assert result.name == "Updated Training"  # Mock object doesn't actually update
        assert mock_db.commit.called

    def test_update_training_not_found(self, mock_db, sample_training_update):
        """Test updating a training that doesn't exist"""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query
        
        result = training_service.update_training(mock_db, 999, sample_training_update)
        
        assert result is None

    def test_delete_training_success(self, mock_db, mock_training):
        """Test deleting a training successfully"""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_training
        mock_db.query.return_value = mock_query
        
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None
        
        result = training_service.delete_training(mock_db, 1)
        
        assert result is True
        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_delete_training_not_found(self, mock_db):
        """Test deleting a training that doesn't exist"""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query
        
        result = training_service.delete_training(mock_db, 999)
        
        assert result is False
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()

    def test_start_training_success(self, mock_db, mock_training, mock_exercise_with_weight):
        """Test starting a training successfully"""
        mock_training.exercises = [mock_exercise_with_weight]
        
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_training
        mock_db.query.return_value = mock_query
        
        mock_db.commit.return_value = None
        
        result = training_service.start_training(mock_db, 1)
        
        assert result is not None
        assert mock_db.commit.called

    def test_finish_training_success(self, mock_db, sample_training_update, mock_training, mock_exercise_with_weight):
        """Test finishing a training successfully"""
        mock_training.exercises = [mock_exercise_with_weight]
        
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_training
        mock_db.query.return_value = mock_query
        
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        result = training_service.finish_training(mock_db, 1, sample_training_update)
        
        assert result is not None
        assert mock_db.commit.called
