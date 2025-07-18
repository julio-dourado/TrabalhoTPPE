# app/services/training_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.training import Training, TrainingStatus
from app.models.exercise import Exercise
from app.schemas.training import (
    TrainingCreate,
    TrainingCreateWithExercises,
    TrainingUpdate,
    TrainingOut,
    TrainingFilters,
    TrainingStatistics,
)
from app.schemas.exercise import ExerciseOut, WithWeightOut, WithoutWeightOut
from app.services.exercise_service import create_exercise


def _convert_exercise_model_to_out_schema(exercise_model: Exercise) -> ExerciseOut:
    """Convert exercise model to output schema"""
    with_weight_out = None
    without_weight_out = None

    if exercise_model.with_weight_details:
        with_weight_out = WithWeightOut.model_validate(
            exercise_model.with_weight_details
        )

    if exercise_model.without_weight_details:
        without_weight_out = WithoutWeightOut.model_validate(
            exercise_model.without_weight_details
        )

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


def _create_exercise_details_in_db(db: Session, exercise_id: int,
                                   exercise_data) -> Exercise:
    """Create exercise details in database"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise ValueError(f"Exercise with id {exercise_id} not found")
    return exercise


def create_training(db: Session, training_data: TrainingCreate,
                    user_id: int) -> TrainingOut:
    """Create a new training"""
    # Create the training instance
    db_training = Training(
        name=training_data.name,
        description=training_data.description,
        category=training_data.category,
        estimated_duration_min=training_data.estimated_duration_min,
        user_id=user_id,
        status=TrainingStatus.PLANNED,
        created_at=datetime.utcnow(),
    )

    # Add exercises to the training
    for exercise_id in training_data.exercises:
        exercise = _create_exercise_details_in_db(db, exercise_id, None)
        db_training.exercises.append(exercise)

    db.add(db_training)
    db.flush()
    db.commit()
    db.refresh(db_training)

    # Convert to output schema
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
        exercises=[
            _convert_exercise_model_to_out_schema(e)
            for e in db_training.exercises
        ],
    )


def create_training_with_exercises(db: Session, training_data: TrainingCreateWithExercises, user_id: int) -> TrainingOut:
    """Create a new training with complete exercise objects"""
    
    # Create the training instance
    db_training = Training(
        name=training_data.name,
        description=training_data.description,
        category=training_data.category,
        estimated_duration_min=training_data.estimated_duration_min,
        user_id=user_id,
        status=TrainingStatus.PLANNED,
        created_at=datetime.utcnow(),
    )

    # Create exercises and add to training
    for exercise_data in training_data.exercises:
        # Create exercise using exercise service
        exercise_out = create_exercise(db, exercise_data)
        
        # Get the exercise from db
        exercise = db.query(Exercise).filter(Exercise.id == exercise_out.id).first()
        db_training.exercises.append(exercise)

    db.add(db_training)
    db.flush()
    db.commit()
    db.refresh(db_training)

    # Convert to output schema
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
        exercises=[
            _convert_exercise_model_to_out_schema(e)
            for e in db_training.exercises
        ],
    )


def get_training_by_id(db: Session, training_id: int) -> Optional[TrainingOut]:
    """Get training by ID"""
    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        return None

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
        exercises=[
            _convert_exercise_model_to_out_schema(e)
            for e in training.exercises
        ],
    )


def get_user_trainings(db: Session, filters: TrainingFilters) -> List[TrainingOut]:
    """Get user trainings with filters"""
    query = db.query(Training)

    if filters.user_id:
        query = query.filter(Training.user_id == filters.user_id)
    if filters.category:
        query = query.filter(Training.category == filters.category)
    if filters.status:
        query = query.filter(Training.status == filters.status)
    if filters.date_from:
        query = query.filter(Training.created_at >= filters.date_from)
    if filters.date_to:
        query = query.filter(Training.created_at <= filters.date_to)

    trainings = query.offset(filters.skip).limit(filters.limit).all()

    return [
        TrainingOut(
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
            exercises=[
                _convert_exercise_model_to_out_schema(e)
                for e in training.exercises
            ],
        )
        for training in trainings
    ]


def update_training(db: Session, training_id: int,
                    training_data: TrainingUpdate) -> Optional[TrainingOut]:
    """Update training"""
    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        return None

    # Update fields
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

    training.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(training)

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
        exercises=[
            _convert_exercise_model_to_out_schema(e)
            for e in training.exercises
        ],
    )


def delete_training(db: Session, training_id: int) -> bool:
    """Delete training"""
    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        return False

    db.delete(training)
    db.commit()
    return True


def start_training(db: Session, training_id: int) -> Optional[TrainingOut]:
    """Start training session"""
    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        return None

    training.status = TrainingStatus.IN_PROGRESS
    training.started_at = datetime.utcnow()
    training.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(training)

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
        exercises=[
            _convert_exercise_model_to_out_schema(e)
            for e in training.exercises
        ],
    )


def finish_training(db: Session, training_id: int,
                    training_data: TrainingUpdate) -> Optional[TrainingOut]:
    """Finish training session"""
    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        return None

    # Update completion data
    training.status = TrainingStatus.COMPLETED
    training.finished_at = datetime.utcnow()
    training.updated_at = datetime.utcnow()

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
        exercises=[
            _convert_exercise_model_to_out_schema(e)
            for e in training.exercises
        ],
    )


def get_training_statistics(db: Session, user_id: int) -> TrainingStatistics:
    """Get training statistics for user"""
    trainings = db.query(Training).filter(Training.user_id == user_id).all()
    completed_trainings = [
        t for t in trainings if t.status == TrainingStatus.COMPLETED
    ]

    total_duration = sum(
        t.actual_duration_min or 0 for t in completed_trainings
    )
    total_calories = sum(
        t.calories_burned or 0 for t in completed_trainings
    )
    total_volume = sum(
        t.total_volume_kg or 0 for t in completed_trainings
    )

    avg_satisfaction = 0
    avg_difficulty = 0
    if completed_trainings:
        satisfaction_scores = [
            t.satisfaction for t in completed_trainings if t.satisfaction
        ]
        difficulty_scores = [
            t.perceived_difficulty for t in completed_trainings
            if t.perceived_difficulty
        ]

        if satisfaction_scores:
            avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
        if difficulty_scores:
            avg_difficulty = sum(difficulty_scores) / len(difficulty_scores)

    # Find most common category
    favorite_category = None
    if completed_trainings:
        categories = [t.category for t in completed_trainings]
        favorite_category = max(set(categories), key=categories.count)

    return TrainingStatistics(
        total_trainings=len(trainings),
        total_duration_min=total_duration,
        total_calories_burned=total_calories,
        total_volume_kg=total_volume,
        average_satisfaction=avg_satisfaction,
        average_difficulty=avg_difficulty,
        completed_trainings=len(completed_trainings),
        favorite_category=favorite_category,
    )
