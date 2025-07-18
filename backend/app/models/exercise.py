from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Text,
    Enum,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class MuscleGroup(str, enum.Enum):
    CHEST = "PEITO"
    BACK = "COSTAS"
    SHOULDERS = "OMBROS"
    BICEPS = "BICEPS"
    TRICEPS = "TRICEPS"
    LEGS = "PERNAS"
    GLUTES = "GLUTEOS"
    ABDOMEN = "ABDOMEN"
    CALVES = "PANTURRILHA"
    FOREARMS = "ANTEBRACO"
    CARDIO = "CARDIO"
    FULL_BODY = "CORPO_INTEIRO"


class ExerciseType(str, enum.Enum):
    WITH_WEIGHT = "COM_PESO"
    WITHOUT_WEIGHT = "SEM_PESO"


class Difficulty(str, enum.Enum):
    BEGINNER = "INICIANTE"
    INTERMEDIATE = "INTERMEDIARIO"
    ADVANCED = "AVANCADO"


class Exercise(Base):
    __tablename__ = "exercicios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    muscle_group = Column(Enum(MuscleGroup), nullable=False)
    difficulty = Column(Enum(Difficulty), default=Difficulty.BEGINNER)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True)
    instructions = Column(Text, nullable=True)  # Detailed execution instructions
    exercise_type = Column(Enum(ExerciseType), nullable=False)

    # User experience fields
    rest_time_sec = Column(Integer, default=60)  # Suggested rest time
    is_compound = Column(Boolean, default=False)  # If it's compound or isolation exercise
    equipment = Column(String(100), nullable=True)  # Required equipment

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (comentados temporariamente)
    # with_weight_details = relationship(
    #     "WithWeight",
    #     back_populates="exercise",
    #     uselist=False,
    #     cascade="all, delete-orphan",
    # )
    # without_weight_details = relationship(
    #     "WithoutWeight",
    #     back_populates="exercise",
    #     uselist=False,
    #     cascade="all, delete-orphan",
    # )
    # trainings = relationship(
    #     "Training", secondary="treino_exercicio", back_populates="exercises"
    # )
    # execution_history = relationship(
    #     "ExecutionHistory", back_populates="exercise", cascade="all, delete-orphan"
    # )


class WithWeight(Base):
    __tablename__ = "com_peso"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercicios.id"), nullable=False)
    weight_kg = Column(Float, nullable=False)
    max_weight_kg = Column(Float, nullable=True)
    suggested_increment_kg = Column(Float, default=2.5)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # exercise = relationship("Exercise", back_populates="with_weight_details")


class WithoutWeight(Base):
    __tablename__ = "sem_peso"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercicios.id"), nullable=False)
    duration_sec = Column(Float, nullable=False)
    distance_m = Column(Float, nullable=False)
    target_speed = Column(Float, nullable=False)
    intensity_level = Column(Integer, default=1)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # exercise = relationship("Exercise", back_populates="without_weight_details")


class ExecutionHistory(Base):
    __tablename__ = "historico_execucao"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercicios.id"), nullable=False)
    training_id = Column(Integer, ForeignKey("treinos.id"), nullable=True)

    # Execution data
    sets_completed = Column(Integer, nullable=False)
    reps_completed = Column(Integer, nullable=False)
    weight_used_kg = Column(Float, nullable=True)
    rest_time_sec = Column(Integer, nullable=True)
    perceived_exertion = Column(Integer, nullable=True)  # 1-10 RPE
    notes = Column(Text, nullable=True)

    # Timestamps
    executed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (comentados temporariamente)
    # user = relationship("User", back_populates="exercise_history")
    # exercise = relationship("Exercise", back_populates="execution_history")
    # training = relationship("Training", back_populates="execution_history")
