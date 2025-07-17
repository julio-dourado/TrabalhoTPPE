from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from datetime import datetime

from app.models.exercise import Exercise, WithWeight, WithoutWeight, ExerciseType
from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseOut,
    WithWeightOut,
    WithoutWeightOut,
)


def _convert_exercise_model_to_out_schema(exercise_model: Exercise) -> ExerciseOut:
    """Convert exercise model to output schema"""
    with_weight_out = None
    without_weight_out = None

    if (
        exercise_model.exercise_type == ExerciseType.WITH_WEIGHT
        and exercise_model.with_weight_details
    ):
        with_weight_out = WithWeightOut.model_validate(exercise_model.with_weight_details)
    elif (
        exercise_model.exercise_type == ExerciseType.WITHOUT_WEIGHT
        and exercise_model.without_weight_details
    ):
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


def _create_exercise_details_in_db(db: Session, exercise: Exercise, exercise_data: ExerciseCreate):
    """Create exercise details based on type"""
    if exercise_data.exercise_type == ExerciseType.WITH_WEIGHT:
        with_weight = WithWeight(
            exercise_id=exercise.id,
            weight_kg=exercise_data.with_weight_details.weight_kg,
            max_weight_kg=exercise_data.with_weight_details.max_weight_kg,
            suggested_increment_kg=exercise_data.with_weight_details.suggested_increment_kg,
        )
        db.add(with_weight)
    else:
        without_weight = WithoutWeight(
            exercise_id=exercise.id,
            duration_sec=exercise_data.without_weight_details.duration_sec,
            distance_m=exercise_data.without_weight_details.distance_m,
            target_speed=exercise_data.without_weight_details.target_speed,
            intensity_level=exercise_data.without_weight_details.intensity_level,
        )
        db.add(without_weight)


def create_exercise(db: Session, exercise_data: ExerciseCreate) -> ExerciseOut:
    """Create a new exercise"""
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

    db.commit()
    db.refresh(db_exercise)

    return _convert_exercise_model_to_out_schema(db_exercise)


def get_exercise_by_id(db: Session, exercise_id: int) -> Optional[ExerciseOut]:
    """Get exercise by ID"""
    stmt = select(Exercise).where(Exercise.id == exercise_id).options(
        selectinload(Exercise.with_weight_details),
        selectinload(Exercise.without_weight_details),
    )
    exercise = db.scalars(stmt).first()

    if not exercise:
        return None

    return _convert_exercise_model_to_out_schema(exercise)


def get_all_exercises(db: Session, skip: int = 0, limit: int = 100) -> List[ExerciseOut]:
    """Get all exercises"""
    stmt = select(Exercise).offset(skip).limit(limit).options(
        selectinload(Exercise.with_weight_details),
        selectinload(Exercise.without_weight_details),
    )
    exercises = db.scalars(stmt).all()

    return [_convert_exercise_model_to_out_schema(exercise) for exercise in exercises]


def update_exercise(db: Session, exercise_id: int, exercise_data: ExerciseUpdate) -> Optional[ExerciseOut]:
    """Update an existing exercise"""
    stmt = select(Exercise).where(Exercise.id == exercise_id).options(
        selectinload(Exercise.with_weight_details),
        selectinload(Exercise.without_weight_details),
    )
    exercise = db.scalars(stmt).first()

    if not exercise:
        return None

    # Update basic fields
    if exercise_data.name is not None:
        exercise.name = exercise_data.name
    if exercise_data.muscle_group is not None:
        exercise.muscle_group = exercise_data.muscle_group
    if exercise_data.difficulty is not None:
        exercise.difficulty = exercise_data.difficulty
    if exercise_data.sets is not None:
        exercise.sets = exercise_data.sets
    if exercise_data.reps is not None:
        exercise.reps = exercise_data.reps
    if exercise_data.comment is not None:
        exercise.comment = exercise_data.comment
    if exercise_data.instructions is not None:
        exercise.instructions = exercise_data.instructions
    if exercise_data.rest_time_sec is not None:
        exercise.rest_time_sec = exercise_data.rest_time_sec
    if exercise_data.is_compound is not None:
        exercise.is_compound = exercise_data.is_compound
    if exercise_data.equipment is not None:
        exercise.equipment = exercise_data.equipment

    # Update exercise details
    if exercise_data.with_weight_details and exercise.with_weight_details:
        if exercise_data.with_weight_details.weight_kg is not None:
            exercise.with_weight_details.weight_kg = exercise_data.with_weight_details.weight_kg
        if exercise_data.with_weight_details.max_weight_kg is not None:
            exercise.with_weight_details.max_weight_kg = exercise_data.with_weight_details.max_weight_kg
        if exercise_data.with_weight_details.suggested_increment_kg is not None:
            exercise.with_weight_details.suggested_increment_kg = exercise_data.with_weight_details.suggested_increment_kg

    if exercise_data.without_weight_details and exercise.without_weight_details:
        if exercise_data.without_weight_details.duration_sec is not None:
            exercise.without_weight_details.duration_sec = exercise_data.without_weight_details.duration_sec
        if exercise_data.without_weight_details.distance_m is not None:
            exercise.without_weight_details.distance_m = exercise_data.without_weight_details.distance_m
        if exercise_data.without_weight_details.target_speed is not None:
            exercise.without_weight_details.target_speed = exercise_data.without_weight_details.target_speed
        if exercise_data.without_weight_details.intensity_level is not None:
            exercise.without_weight_details.intensity_level = exercise_data.without_weight_details.intensity_level

    exercise.updated_at = datetime.now()

    db.commit()
    db.refresh(exercise)

    return _convert_exercise_model_to_out_schema(exercise)


def delete_exercise(db: Session, exercise_id: int) -> bool:
    """Delete an exercise"""
    stmt = select(Exercise).where(Exercise.id == exercise_id)
    exercise = db.scalars(stmt).first()

    if not exercise:
        return False

    db.delete(exercise)
    db.commit()

    return True


def get_exercises_by_muscle_group(db: Session, muscle_group: str) -> List[ExerciseOut]:
    """Get exercises by muscle group"""
    stmt = select(Exercise).where(Exercise.muscle_group == muscle_group).options(
        selectinload(Exercise.with_weight_details),
        selectinload(Exercise.without_weight_details),
    )
    exercises = db.scalars(stmt).all()

    return [_convert_exercise_model_to_out_schema(exercise) for exercise in exercises]


def get_exercises_by_difficulty(db: Session, difficulty: str) -> List[ExerciseOut]:
    """Get exercises by difficulty"""
    stmt = select(Exercise).where(Exercise.difficulty == difficulty).options(
        selectinload(Exercise.with_weight_details),
        selectinload(Exercise.without_weight_details),
    )
    exercises = db.scalars(stmt).all()

    return [_convert_exercise_model_to_out_schema(exercise) for exercise in exercises]
