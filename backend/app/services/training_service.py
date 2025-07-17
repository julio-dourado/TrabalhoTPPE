from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from datetime import datetime

from app.models.training import Training, TrainingStatus
from app.models.exercise import Exercise, WithWeight, WithoutWeight
from app.schemas.training import TrainingCreate, TrainingUpdate, TrainingOut
from app.schemas.exercise import ExerciseOut, WithWeightOut, WithoutWeightOut


def _convert_exercise_model_to_out_schema(exercise_model: Exercise) -> ExerciseOut:
    """Convert exercise model to output schema"""
    with_weight_out = None
    without_weight_out = None

    if exercise_model.with_weight_details:
        with_weight_out = WithWeightOut.model_validate(exercise_model.with_weight_details)
    
    if exercise_model.without_weight_details:
        without_weight_out = WithoutWeightOut.model_validate(exercise_model.without_weight_details)

    return ExerciseOut(
        id=exercise_model.id,
        name=exercise_model.name,
        muscle_group=exercise_model.muscle_group,
        difficulty=exercise_model.difficulty,
        sets=exercise_model.sets,
        reps=exercise_model.reps,
        comment=exercise_model.comment,
        instructions=exercise_model.instructions,
        rest_time_sec=exercise_model.rest_time_sec,
        is_compound=exercise_model.is_compound,
        equipment=exercise_model.equipment,
        exercise_type=exercise_model.exercise_type,
        with_weight_details=with_weight_out,
        without_weight_details=without_weight_out,
        created_at=exercise_model.created_at,
        updated_at=exercise_model.updated_at,
    )


def _create_exercise_details_in_db(db: Session, exercise: Exercise, exercise_data):
    """Create exercise details based on type"""
    if exercise_data.with_weight_details:
        with_weight = WithWeight(
            exercise_id=exercise.id,
            weight_kg=exercise_data.with_weight_details.weight_kg,
            max_weight_kg=exercise_data.with_weight_details.max_weight_kg,
            suggested_increment_kg=exercise_data.with_weight_details.suggested_increment_kg,
        )
        db.add(with_weight)
    
    if exercise_data.without_weight_details:
        without_weight = WithoutWeight(
            exercise_id=exercise.id,
            duration_sec=exercise_data.without_weight_details.duration_sec,
            distance_m=exercise_data.without_weight_details.distance_m,
            target_speed=exercise_data.without_weight_details.target_speed,
            intensity_level=exercise_data.without_weight_details.intensity_level,
        )
        db.add(without_weight)


def create_training(
    db: Session, training_data: TrainingCreate, current_user_id: int
) -> TrainingOut:
    """Create a new training"""
    db_training = Training(
        name=training_data.name,
        description=training_data.description,
        category=training_data.category,
        estimated_duration_min=training_data.estimated_duration_min,
        user_id=current_user_id
    )
    db.add(db_training)
    db.flush()

    for exercise_data in training_data.exercises:
        db_exercise = Exercise(
            name=exercise_data.name,
            muscle_group=exercise_data.muscle_group,
            difficulty=exercise_data.difficulty,
            sets=exercise_data.sets,
            reps=exercise_data.reps,
            comment=exercise_data.comment,
            instructions=exercise_data.instructions,
            rest_time_sec=exercise_data.rest_time_sec,
            is_compound=exercise_data.is_compound,
            equipment=exercise_data.equipment,
            exercise_type=exercise_data.exercise_type,
        )
        db.add(db_exercise)
        db.flush()

        _create_exercise_details_in_db(db, db_exercise, exercise_data)

        db_training.exercises.append(db_exercise)

    db.commit()
    db.refresh(db_training)

    exercises_out = [
        _convert_exercise_model_to_out_schema(e) for e in db_training.exercises
    ]

    return TrainingOut(
        id=db_training.id,
        name=db_training.name,
        description=db_training.description,
        category=db_training.category,
        estimated_duration_min=db_training.estimated_duration_min,
        user_id=db_training.user_id,
        status=db_training.status,
        actual_duration_min=db_training.actual_duration_min,
        calories_burned=db_training.calories_burned,
        total_volume_kg=db_training.total_volume_kg,
        perceived_difficulty=db_training.perceived_difficulty,
        satisfaction=db_training.satisfaction,
        observations=db_training.observations,
        created_at=db_training.created_at,
        updated_at=db_training.updated_at,
        started_at=db_training.started_at,
        finished_at=db_training.finished_at,
        exercises=exercises_out,
    )


def get_training_by_id(db: Session, training_id: int) -> Optional[TrainingOut]:
    """Get training by ID"""
    stmt = select(Training).where(Training.id == training_id).options(
        selectinload(Training.exercises).selectinload(Exercise.with_weight_details),
        selectinload(Training.exercises).selectinload(Exercise.without_weight_details),
    )
    training = db.scalars(stmt).first()

    if not training:
        return None

    exercises_out = [
        _convert_exercise_model_to_out_schema(e) for e in training.exercises
    ]

    return TrainingOut(
        id=training.id,
        name=training.name,
        description=training.description,
        category=training.category,
        estimated_duration_min=training.estimated_duration_min,
        user_id=training.user_id,
        status=training.status,
        actual_duration_min=training.actual_duration_min,
        calories_burned=training.calories_burned,
        total_volume_kg=training.total_volume_kg,
        perceived_difficulty=training.perceived_difficulty,
        satisfaction=training.satisfaction,
        observations=training.observations,
        created_at=training.created_at,
        updated_at=training.updated_at,
        started_at=training.started_at,
        finished_at=training.finished_at,
        exercises=exercises_out,
    )


def get_user_trainings(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[TrainingOut]:
    """Get user trainings"""
    stmt = select(Training).where(Training.user_id == user_id).offset(skip).limit(limit).options(
        selectinload(Training.exercises).selectinload(Exercise.with_weight_details),
        selectinload(Training.exercises).selectinload(Exercise.without_weight_details),
    )
    trainings = db.scalars(stmt).all()

    result = []
    for training in trainings:
        exercises_out = [
            _convert_exercise_model_to_out_schema(e) for e in training.exercises
        ]
        
        result.append(TrainingOut(
            id=training.id,
            name=training.name,
            description=training.description,
            category=training.category,
            estimated_duration_min=training.estimated_duration_min,
            user_id=training.user_id,
            status=training.status,
            actual_duration_min=training.actual_duration_min,
            calories_burned=training.calories_burned,
            total_volume_kg=training.total_volume_kg,
            perceived_difficulty=training.perceived_difficulty,
            satisfaction=training.satisfaction,
            observations=training.observations,
            created_at=training.created_at,
            updated_at=training.updated_at,
            started_at=training.started_at,
            finished_at=training.finished_at,
            exercises=exercises_out,
        ))

    return result


def update_training(db: Session, training_id: int, training_data: TrainingUpdate) -> Optional[TrainingOut]:
    """Update training"""
    stmt = select(Training).where(Training.id == training_id).options(
        selectinload(Training.exercises).selectinload(Exercise.with_weight_details),
        selectinload(Training.exercises).selectinload(Exercise.without_weight_details),
    )
    training = db.scalars(stmt).first()

    if not training:
        return None

    # Update fields if provided
    if training_data.name is not None:
        training.name = training_data.name
    if training_data.description is not None:
        training.description = training_data.description
    if training_data.category is not None:
        training.category = training_data.category
    if training_data.estimated_duration_min is not None:
        training.estimated_duration_min = training_data.estimated_duration_min
    if training_data.status is not None:
        training.status = training_data.status
    if training_data.actual_duration_min is not None:
        training.actual_duration_min = training_data.actual_duration_min
    if training_data.calories_burned is not None:
        training.calories_burned = training_data.calories_burned
    if training_data.total_volume_kg is not None:
        training.total_volume_kg = training_data.total_volume_kg
    if training_data.perceived_difficulty is not None:
        training.perceived_difficulty = training_data.perceived_difficulty
    if training_data.satisfaction is not None:
        training.satisfaction = training_data.satisfaction
    if training_data.observations is not None:
        training.observations = training_data.observations

    training.updated_at = datetime.now()

    db.commit()
    db.refresh(training)

    exercises_out = [
        _convert_exercise_model_to_out_schema(e) for e in training.exercises
    ]

    return TrainingOut(
        id=training.id,
        name=training.name,
        description=training.description,
        category=training.category,
        estimated_duration_min=training.estimated_duration_min,
        user_id=training.user_id,
        status=training.status,
        actual_duration_min=training.actual_duration_min,
        calories_burned=training.calories_burned,
        total_volume_kg=training.total_volume_kg,
        perceived_difficulty=training.perceived_difficulty,
        satisfaction=training.satisfaction,
        observations=training.observations,
        created_at=training.created_at,
        updated_at=training.updated_at,
        started_at=training.started_at,
        finished_at=training.finished_at,
        exercises=exercises_out,
    )


def delete_training(db: Session, training_id: int) -> bool:
    """Delete training"""
    stmt = select(Training).where(Training.id == training_id)
    training = db.scalars(stmt).first()

    if not training:
        return False

    db.delete(training)
    db.commit()

    return True


def start_training(db: Session, training_id: int) -> Optional[TrainingOut]:
    """Start a training"""
    training = get_training_by_id(db, training_id)
    
    if not training:
        return None
    
    # Update training status to IN_PROGRESS
    update_data = TrainingUpdate(
        status=TrainingStatus.IN_PROGRESS
    )
    
    # Get the actual model to update started_at
    stmt = select(Training).where(Training.id == training_id)
    db_training = db.scalars(stmt).first()
    
    if db_training:
        db_training.status = TrainingStatus.IN_PROGRESS
        db_training.started_at = datetime.now()
        db_training.updated_at = datetime.now()
        db.commit()
    
    return get_training_by_id(db, training_id)


def finish_training(db: Session, training_id: int, training_data: TrainingUpdate) -> Optional[TrainingOut]:
    """Finish a training"""
    stmt = select(Training).where(Training.id == training_id)
    training = db.scalars(stmt).first()

    if not training:
        return None

    # Update training with completion data
    training.status = TrainingStatus.COMPLETED
    training.finished_at = datetime.now()
    training.updated_at = datetime.now()
    
    if training_data.actual_duration_min is not None:
        training.actual_duration_min = training_data.actual_duration_min
    if training_data.calories_burned is not None:
        training.calories_burned = training_data.calories_burned
    if training_data.total_volume_kg is not None:
        training.total_volume_kg = training_data.total_volume_kg
    if training_data.perceived_difficulty is not None:
        training.perceived_difficulty = training_data.perceived_difficulty
    if training_data.satisfaction is not None:
        training.satisfaction = training_data.satisfaction
    if training_data.observations is not None:
        training.observations = training_data.observations

    db.commit()
    db.refresh(training)

    return get_training_by_id(db, training_id)
