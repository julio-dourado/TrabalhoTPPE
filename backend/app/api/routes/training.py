from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.training import TrainingCreate, TrainingUpdate, TrainingOut
from app.services.training_service import (
    create_training,
    get_training_by_id,
    get_user_trainings,
    update_training,
    delete_training,
    start_training,
    finish_training,
)

router = APIRouter()


@router.post("/", response_model=TrainingOut, status_code=status.HTTP_201_CREATED)
def create_new_training(
    training_data: TrainingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new training"""
    try:
        return create_training(db, training_data, current_user.id)
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
    """Get user trainings"""
    return get_user_trainings(db, current_user.id, skip=skip, limit=limit)


@router.get("/{training_id}", response_model=TrainingOut)
def get_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get training by ID"""
    training = get_training_by_id(db, training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    # Check if the training belongs to the current user
    if training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
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
    # First check if training exists and belongs to user
    training = get_training_by_id(db, training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    if training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    updated_training = update_training(db, training_id, training_data)
    if not updated_training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    return updated_training


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a training"""
    # First check if training exists and belongs to user
    training = get_training_by_id(db, training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    if training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    success = delete_training(db, training_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )


@router.post("/{training_id}/start", response_model=TrainingOut)
def start_training_endpoint(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start a training"""
    # First check if training exists and belongs to user
    training = get_training_by_id(db, training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    if training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    started_training = start_training(db, training_id)
    if not started_training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    return started_training


@router.post("/{training_id}/finish", response_model=TrainingOut)
def finish_training_endpoint(
    training_id: int,
    training_data: TrainingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Finish a training"""
    # First check if training exists and belongs to user
    training = get_training_by_id(db, training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    if training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    finished_training = finish_training(db, training_id, training_data)
    if not finished_training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found",
        )
    
    return finished_training 