from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    DateTime,
    Text,
    Enum,
    Float,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class TrainingStatus(str, enum.Enum):
    PLANNED = "PLANEJADO"
    IN_PROGRESS = "EM_ANDAMENTO"
    COMPLETED = "CONCLUIDO"
    PAUSED = "PAUSADO"
    CANCELLED = "CANCELADO"


class TrainingCategory(str, enum.Enum):
    STRENGTH = "FORCA"
    CARDIO = "CARDIO"
    FLEXIBILITY = "FLEXIBILIDADE"
    FUNCTIONAL = "FUNCIONAL"
    ENDURANCE = "RESISTENCIA"
    SPORTS = "ESPORTES"
    REHABILITATION = "REABILITACAO"


training_exercise_link = Table(
    "treino_exercicio",
    Base.metadata,
    Column("treino_id", Integer, ForeignKey("treinos.id"), primary_key=True),
    Column("exercicio_id", Integer, ForeignKey("exercicios.id"), primary_key=True),
)


class Training(Base):
    __tablename__ = "treinos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(TrainingCategory), default=TrainingCategory.STRENGTH)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Status and control
    status = Column(Enum(TrainingStatus), default=TrainingStatus.PLANNED)
    estimated_duration_min = Column(Integer, default=60)
    actual_duration_min = Column(Integer, nullable=True)

    # Statistics
    calories_burned = Column(Float, nullable=True)
    total_volume_kg = Column(Float, nullable=True)  # Total weight lifted

    # Evaluation
    perceived_difficulty = Column(Integer, nullable=True)  # 1-10 (RPE)
    satisfaction = Column(Integer, nullable=True)  # 1-5 stars
    observations = Column(Text, nullable=True)

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (comentados temporariamente)
    # user = relationship("User", back_populates="trainings")
    # exercises = relationship(
    #     "Exercise", secondary=training_exercise_link, back_populates="trainings"
    # )
    # execution_history = relationship(
    #     "ExecutionHistory", back_populates="training", cascade="all, delete-orphan"
    # )


class TrainingTemplate(Base):
    __tablename__ = "template_treino"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(TrainingCategory), default=TrainingCategory.STRENGTH)
    creator_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Template settings
    is_public = Column(Boolean, default=False)  # False = private, True = public
    estimated_duration_min = Column(Integer, default=60)
    difficulty_level = Column(String(20), default="beginner")

    # Usage statistics
    times_used = Column(Integer, default=0)
    average_rating = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (comentados temporariamente)
    # creator = relationship("User", back_populates="training_templates")
    # exercise_templates = relationship(
    #     "ExerciseTemplate", back_populates="template", cascade="all, delete-orphan"
    # )


class ExerciseTemplate(Base):
    __tablename__ = "exercicio_template"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("template_treino.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercicios.id"), nullable=False)

    # Template specific settings
    order_in_template = Column(Integer, nullable=False)
    suggested_sets = Column(Integer, nullable=False)
    suggested_reps = Column(Integer, nullable=False)
    suggested_weight_kg = Column(Float, nullable=True)
    suggested_rest_time_sec = Column(Integer, default=60)
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (comentados temporariamente)
    # template = relationship("TrainingTemplate", back_populates="exercise_templates")
    # exercise = relationship("Exercise")
