# app/schemas/exercise.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.exercise import MuscleGroup, Difficulty, ExerciseType


class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, example="Bench Press")
    muscle_group: MuscleGroup = Field(..., example=MuscleGroup.CHEST)
    difficulty: Difficulty = Field(..., example=Difficulty.INTERMEDIATE)
    sets: int = Field(..., gt=0, le=20, example=3)
    reps: int = Field(..., gt=0, le=500, example=10)
    comment: Optional[str] = Field(None, max_length=500, example="Focus on form.")
    instructions: Optional[str] = Field(
        None, max_length=2000, example="Lie down on bench, lower bar to chest"
    )
    rest_time_sec: int = Field(..., ge=0, le=600, example=90)
    is_compound: bool = Field(..., example=True)
    equipment: Optional[str] = Field(None, max_length=100, example="Barbell")
    exercise_type: ExerciseType = Field(..., example=ExerciseType.WITH_WEIGHT)


class WithWeightBase(BaseModel):
    weight_kg: float = Field(..., gt=0, le=1000, example=80.0)
    max_weight_kg: Optional[float] = Field(None, gt=0, le=1000, example=100.0)
    suggested_increment_kg: float = Field(..., gt=0, le=50, example=2.5)


class WithWeightCreate(WithWeightBase):
    pass


class WithWeightUpdate(BaseModel):
    weight_kg: Optional[float] = Field(None, gt=0, le=1000)
    max_weight_kg: Optional[float] = Field(None, gt=0, le=1000)
    suggested_increment_kg: Optional[float] = Field(None, gt=0, le=50)


class WithWeightOut(WithWeightBase):
    id: int
    exercise_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WithoutWeightBase(BaseModel):
    duration_sec: float = Field(..., gt=0, le=86400, example=1800.0)
    distance_m: float = Field(..., ge=0, le=100000, example=5000.0)
    target_speed: float = Field(..., gt=0, le=100, example=10.0)
    intensity_level: int = Field(..., ge=1, le=10, example=5)


class WithoutWeightCreate(WithoutWeightBase):
    duration_sec: Optional[float] = Field(None, gt=0, le=86400)
    distance_m: Optional[float] = Field(None, ge=0, le=100000)
    target_speed: Optional[float] = Field(None, gt=0, le=100)
    intensity_level: Optional[int] = Field(None, ge=1, le=10)


class WithoutWeightUpdate(BaseModel):
    duration_sec: Optional[float] = Field(None, gt=0, le=86400)
    distance_m: Optional[float] = Field(None, ge=0, le=100000)
    target_speed: Optional[float] = Field(None, gt=0, le=100)
    intensity_level: Optional[int] = Field(None, ge=1, le=10)


class WithoutWeightOut(WithoutWeightBase):
    id: int
    exercise_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExerciseCreate(ExerciseBase):
    with_weight_details: Optional[WithWeightCreate] = None
    without_weight_details: Optional[WithoutWeightCreate] = None


class ExerciseOut(ExerciseBase):
    id: int
    with_weight_details: Optional[WithWeightOut] = None
    without_weight_details: Optional[WithoutWeightOut] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=255, example="Bench Press"
    )
    muscle_group: Optional[MuscleGroup] = None
    difficulty: Optional[Difficulty] = None
    sets: Optional[int] = Field(None, gt=0, le=20, example=3)
    reps: Optional[int] = Field(None, gt=0, le=500, example=10)
    comment: Optional[str] = Field(None, max_length=500, example="Focus on form.")
    instructions: Optional[str] = Field(None, max_length=2000)
    rest_time_sec: Optional[int] = Field(None, ge=0, le=600)
    is_compound: Optional[bool] = None
    equipment: Optional[str] = Field(None, max_length=100)
    with_weight_details: Optional[WithWeightUpdate] = None
    without_weight_details: Optional[WithoutWeightUpdate] = None

    class Config:
        from_attributes = True
