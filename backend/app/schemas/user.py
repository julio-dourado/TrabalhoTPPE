from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import Gender, ActivityLevel, FitnessGoal


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    birth_date: Optional[date] = None
    gender: Gender = Field(default=Gender.NOT_INFORMED)
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=20, le=500)
    activity_level: ActivityLevel = Field(default=ActivityLevel.SEDENTARY)
    main_goal: FitnessGoal = Field(default=FitnessGoal.GENERAL_HEALTH)
    training_experience_years: float = Field(default=0.0, ge=0, le=50)
    bio: Optional[str] = Field(None, max_length=1000)
    target_weight_kg: Optional[float] = Field(None, ge=20, le=500)

    model_config = ConfigDict(extra="forbid")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    password: Optional[str] = Field(None, min_length=8)
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=20, le=500)
    activity_level: Optional[ActivityLevel] = None
    main_goal: Optional[FitnessGoal] = None
    training_experience_years: Optional[float] = Field(None, ge=0, le=50)
    bio: Optional[str] = Field(None, max_length=1000)
    target_weight_kg: Optional[float] = Field(None, ge=20, le=500)

    model_config = ConfigDict(extra="forbid")


class UserOut(UserBase):
    id: int
    birth_date: Optional[date] = None
    gender: Gender
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: ActivityLevel
    main_goal: FitnessGoal
    training_experience_years: float
    bio: Optional[str] = None
    target_weight_kg: Optional[float] = None
    is_active: bool
    is_premium: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
