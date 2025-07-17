from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseOut
from app.services.exercise_service import (
    create_exercise,
    get_exercise_by_id,
    get_all_exercises,
    update_exercise,
    delete_exercise,
    get_exercises_by_muscle_group,
    get_exercises_by_difficulty,
)

router = APIRouter()


@router.post("/", response_model=ExerciseOut,
             status_code=status.HTTP_201_CREATED)
def create_new_exercise(
    exercise_data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new exercise"""
    try:
        return create_exercise(db, exercise_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating exercise: {str(e)}",
        )


@router.get("/", response_model=List[ExerciseOut])
def get_exercises(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all exercises"""
    return get_all_exercises(db, skip=skip, limit=limit)


@router.get("/{exercise_id}", response_model=ExerciseOut)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get exercise by ID"""
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        )
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseOut)
def update_existing_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing exercise"""
    exercise = update_exercise(db, exercise_id, exercise_data)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        )
    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an exercise"""
    success = delete_exercise(db, exercise_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        )


@router.get("/muscle-group/{muscle_group}", response_model=List[ExerciseOut])
def get_exercises_by_muscle_group_endpoint(
    muscle_group: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get exercises by muscle group"""
    return get_exercises_by_muscle_group(db, muscle_group)


@router.get("/difficulty/{difficulty}", response_model=List[ExerciseOut])
def get_exercises_by_difficulty_endpoint(
    difficulty: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get exercises by difficulty"""
    return get_exercises_by_difficulty(db, difficulty) 