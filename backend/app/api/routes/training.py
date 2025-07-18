from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.training import (
    TrainingCreate,
    TrainingCreateWithExercises,
    TrainingUpdate,
    TrainingOut,
    TrainingFilters,
    TrainingStatistics,
)
from app.services.training_service import (
    create_training,
    create_training_with_exercises,
    get_training_by_id,
    get_user_trainings,
    update_training,
    delete_training,
    start_training,
    finish_training,
    get_training_statistics,
)

router = APIRouter()


@router.post("/", response_model=TrainingOut,
             status_code=status.HTTP_201_CREATED)
def create_new_training(
    training_data: TrainingCreateWithExercises,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new training"""
    try:
        return create_training_with_exercises(db, training_data, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating training: {str(e)}",
        )


@router.get("/", response_model=List[TrainingOut])
def get_trainings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all trainings for the current user"""
    filters = TrainingFilters(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    return get_user_trainings(db, filters)


@router.get("/statistics", response_model=TrainingStatistics)
def get_user_training_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get training statistics for the current user"""
    return get_training_statistics(db, current_user.id)


@router.get("/{training_id}", response_model=TrainingOut)
def get_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get training by ID"""
    training = get_training_by_id(db, training_id)
    if not training or training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    return training


@router.put("/{training_id}", response_model=TrainingOut)
def update_existing_training(
    training_id: int,
    training_data: TrainingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing training"""
    training = update_training(db, training_id, training_data)
    if not training or training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    return training


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a training"""
    success = delete_training(db, training_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )


@router.post("/{training_id}/start", response_model=TrainingOut)
def start_training_session(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start a training session"""
    training = start_training(db, training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    return training


@router.post("/{training_id}/finish", response_model=TrainingOut)
def finish_training_session(
    training_id: int,
    training_data: TrainingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Finish a training session"""
    training = finish_training(db, training_id, training_data)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    return training 