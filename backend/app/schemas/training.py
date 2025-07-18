from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.exercise import ExerciseOut, ExerciseCreate
from app.models.training import TrainingCategory, TrainingStatus


class TrainingBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(
        None, max_length=1000, example="Full body workout"
    )
    category: TrainingCategory = Field(..., example=TrainingCategory.STRENGTH)
    estimated_duration_min: int = Field(
        ..., ge=15, le=300, example=60
    )


class TrainingCreate(TrainingBase):
    exercises: List[int] = Field(
        default_factory=list, description="List of exercise IDs"
    )


class TrainingCreateWithExercises(TrainingBase):
    exercises: List[ExerciseCreate] = Field(
        default_factory=list, description="List of complete exercise objects"
    )


class TrainingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[TrainingCategory] = None
    estimated_duration_min: Optional[int] = Field(None, ge=15, le=300)
    status: Optional[TrainingStatus] = None
    exercises: Optional[List[int]] = None
    # For session completion
    actual_duration_min: Optional[int] = Field(None, ge=1, le=600)
    calories_burned: Optional[float] = Field(None, ge=0, le=2000)
    total_volume_kg: Optional[float] = Field(None, ge=0, le=50000)
    # Rating fields (1-10 scale for difficulty, 1-5 for satisfaction)
    perceived_difficulty: Optional[int] = Field(
        None, ge=1, le=10, example=7
    )
    satisfaction: Optional[int] = Field(
        None, ge=1, le=5, example=4
    )
    observations: Optional[str] = Field(None, max_length=1000)


class TrainingOut(TrainingBase):
    id: int
    user_id: int
    status: TrainingStatus
    actual_duration_min: Optional[int] = None
    calories_burned: Optional[float] = None
    total_volume_kg: Optional[float] = None
    perceived_difficulty: Optional[int] = None
    satisfaction: Optional[int] = None
    observations: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    exercises: List[ExerciseOut]

    class Config:
        from_attributes = True


class TrainingStatistics(BaseModel):
    total_trainings: int = Field(
        ..., ge=0, description="Total number of trainings"
    )
    total_duration_min: int = Field(
        ..., ge=0, description="Total training duration in minutes"
    )
    total_calories_burned: float = Field(
        ..., ge=0, description="Total calories burned"
    )
    total_volume_kg: float = Field(
        ..., ge=0, description="Total volume lifted in kg"
    )
    actual_duration_min: Optional[int] = None
    average_satisfaction: float = Field(
        ..., ge=0, le=5, description="Average satisfaction rating"
    )
    average_difficulty: float = Field(
        ..., ge=0, le=10, description="Average difficulty rating"
    )
    completed_trainings: int = Field(
        ..., ge=0, description="Number of completed trainings"
    )
    favorite_category: Optional[TrainingCategory] = None

    class Config:
        from_attributes = True


class TrainingFilters(BaseModel):
    user_id: Optional[int] = None
    category: Optional[TrainingCategory] = None
    status: Optional[TrainingStatus] = None
    min_duration: Optional[int] = Field(None, ge=1)
    max_duration: Optional[int] = Field(None, ge=1)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=100)
