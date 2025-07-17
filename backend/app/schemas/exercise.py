from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from app.models.exercise import MuscleGroup, Difficulty, ExerciseType


class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, example="Squat")
    muscle_group: MuscleGroup = Field(..., example=MuscleGroup.LEGS)
    difficulty: Difficulty = Field(default=Difficulty.BEGINNER)
    sets: int = Field(..., gt=0, le=20, example=3)
    reps: int = Field(..., gt=0, le=500, example=10)
    comment: Optional[str] = Field(None, max_length=500, example="Focus on form.")
    instructions: Optional[str] = Field(
        None,
        max_length=2000,
        example="Keep your feet shoulder-width apart...",
    )
    rest_time_sec: int = Field(default=60, ge=0, le=600)
    is_compound: bool = Field(
        default=False, description="Whether it's a compound (True) or isolation (False) exercise"
    )
    equipment: Optional[str] = Field(None, max_length=100, example="Olympic barbell")


class WithWeightBase(BaseModel):
    weight_kg: float = Field(..., gt=0, le=1000, example=80.0)
    max_weight_kg: Optional[float] = Field(None, gt=0, le=1000, example=100.0)
    suggested_increment_kg: float = Field(default=2.5, gt=0, le=50)

    @field_validator("max_weight_kg")
    @classmethod
    def validate_max_weight(cls, v, info):
        if v is not None and "weight_kg" in info.data:
            if v < info.data["weight_kg"]:
                raise ValueError("Max weight must be greater than or equal to current weight")
        return v


class WithWeightCreate(WithWeightBase):
    pass


class WithWeightUpdate(BaseModel):
    weight_kg: Optional[float] = Field(None, gt=0, le=1000)
    max_weight_kg: Optional[float] = Field(None, gt=0, le=1000)
    suggested_increment_kg: Optional[float] = Field(None, gt=0, le=50)

    @field_validator("max_weight_kg")
    @classmethod
    def validate_max_weight(cls, v, info):
        if v is not None and "weight_kg" in info.data:
            if v < info.data["weight_kg"]:
                raise ValueError("Max weight must be greater than or equal to current weight")
        return v


class WithWeightOut(WithWeightBase):
    id: int
    exercise_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class WithoutWeightBase(BaseModel):
    duration_sec: float = Field(..., gt=0, le=86400, example=30.0)
    distance_m: float = Field(..., ge=0, le=100000, example=1000.0)
    target_speed: float = Field(..., gt=0, le=100, example=10.0)
    intensity_level: int = Field(default=1, ge=1, le=10)


class WithoutWeightCreate(WithoutWeightBase):
    pass


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

    model_config = ConfigDict(from_attributes=True)


class ExerciseCreate(ExerciseBase):
    exercise_type: ExerciseType
    with_weight_details: Optional[WithWeightCreate] = None
    without_weight_details: Optional[WithoutWeightCreate] = None

    @model_validator(mode="after")
    def validate_exercise_details(self):
        if self.exercise_type == ExerciseType.WITH_WEIGHT:
            if not self.with_weight_details:
                raise ValueError("With weight details are required for WITH_WEIGHT exercises")
            if self.without_weight_details:
                raise ValueError("Cannot have without weight details for WITH_WEIGHT exercises")
        elif self.exercise_type == ExerciseType.WITHOUT_WEIGHT:
            if not self.without_weight_details:
                raise ValueError("Without weight details are required for WITHOUT_WEIGHT exercises")
            if self.with_weight_details:
                raise ValueError("Cannot have with weight details for WITHOUT_WEIGHT exercises")
        return self

    model_config = ConfigDict(extra="forbid")


class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=255, example="Squat"
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

    model_config = ConfigDict(extra="forbid")


class ExerciseOut(ExerciseBase):
    id: int
    exercise_type: ExerciseType
    with_weight_details: Optional[WithWeightOut] = None
    without_weight_details: Optional[WithoutWeightOut] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ExerciseSummary(BaseModel):
    """Simplified exercise data for lists"""
    id: int
    name: str
    muscle_group: MuscleGroup
    difficulty: Difficulty
    sets: int
    reps: int
    exercise_type: ExerciseType

    model_config = ConfigDict(from_attributes=True)


class ExerciseFilter(BaseModel):
    """Filter options for exercise searches"""
    muscle_group: Optional[MuscleGroup] = None
    difficulty: Optional[Difficulty] = None
    exercise_type: Optional[ExerciseType] = None
    is_compound: Optional[bool] = None
    equipment: Optional[str] = None
