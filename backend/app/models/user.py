from sqlalchemy import Column, Integer, String, Float, Date, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class Gender(str, enum.Enum):
    MALE = "masculino"
    FEMALE = "feminino"
    OTHER = "outro"
    NOT_INFORMED = "nao_informado"


class ActivityLevel(str, enum.Enum):
    SEDENTARY = "sedentario"
    LIGHT = "leve"
    MODERATE = "moderado"
    INTENSE = "intenso"
    VERY_INTENSE = "muito_intenso"


class FitnessGoal(str, enum.Enum):
    WEIGHT_LOSS = "perda_peso"
    MUSCLE_GAIN = "ganho_massa"
    GENERAL_HEALTH = "saude_geral"
    STRENGTH = "forca"
    ENDURANCE = "resistencia"


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Physical profile
    birth_date = Column(Date, nullable=True)
    gender = Column(Enum(Gender), default=Gender.NOT_INFORMED)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)

    # Fitness profile
    activity_level = Column(Enum(ActivityLevel), default=ActivityLevel.SEDENTARY)
    main_goal = Column(Enum(FitnessGoal), default=FitnessGoal.GENERAL_HEALTH)
    training_experience_years = Column(Float, default=0.0)

    # Additional information
    bio = Column(Text, nullable=True)
    target_weight_kg = Column(Float, nullable=True)

    # App settings
    is_active = Column(Integer, default=1)
    is_premium = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    trainings = relationship(
        "Training", back_populates="user", cascade="all, delete-orphan"
    )
    exercise_history = relationship(
        "ExecutionHistory", back_populates="user", cascade="all, delete-orphan"
    )
    training_templates = relationship(
        "TrainingTemplate", back_populates="creator", cascade="all, delete-orphan"
    )
