from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.user import UserOut
from app.schemas.exercise import ExerciseCreate, ExerciseOut, ExerciseSummary
from app.models.training import TrainingStatus, TrainingCategory


class TrainingBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, example="Leg Training")
    description: Optional[str] = Field(
        None, max_length=1000, example="Strength training focused on lower body"
    )
    category: TrainingCategory = Field(default=TrainingCategory.STRENGTH)
    estimated_duration_min: int = Field(
        default=60, ge=15, le=300, description="Estimated duration in minutes"
    )


class TrainingCreate(TrainingBase):
    exercises: List[ExerciseCreate] = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


class TrainingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[TrainingCategory] = None
    estimated_duration_min: Optional[int] = Field(None, ge=15, le=300)
    status: Optional[TrainingStatus] = None

    # Execution fields
    actual_duration_min: Optional[int] = Field(None, ge=1, le=600)
    calories_burned: Optional[float] = Field(None, ge=0, le=2000)
    total_volume_kg: Optional[float] = Field(None, ge=0, le=50000)

    # Evaluation
    perceived_difficulty: Optional[int] = Field(
        None, ge=1, le=10, description="RPE - Rate of Perceived Exertion"
    )
    satisfaction: Optional[int] = Field(
        None, ge=1, le=5, description="Satisfaction level (1-5)"
    )
    observations: Optional[str] = Field(None, max_length=1000)

    model_config = ConfigDict(extra="forbid")


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
    exercises: List[ExerciseOut] = []

    model_config = ConfigDict(from_attributes=True)


class TrainingSummary(BaseModel):
    """Simplified training data for lists"""
    id: int
    name: str
    category: TrainingCategory
    status: TrainingStatus
    estimated_duration_min: int
    actual_duration_min: Optional[int] = None
    created_at: datetime
    exercise_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class TrainingStats(BaseModel):
    """Training statistics for dashboard"""
    total_trainings: int = 0
    completed_trainings: int = 0
    total_duration_min: int = 0
    average_duration_min: float = 0
    total_calories_burned: float = 0
    total_volume_kg: float = 0
    favorite_category: Optional[TrainingCategory] = None
    current_streak_days: int = 0
    best_streak_days: int = 0


class TrainingFilter(BaseModel):
    """Filter options for training searches"""
    category: Optional[TrainingCategory] = None
    status: Optional[TrainingStatus] = None
    min_duration: Optional[int] = Field(None, ge=1)
    max_duration: Optional[int] = Field(None, ge=1)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
