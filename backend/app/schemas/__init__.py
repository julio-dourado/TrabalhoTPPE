# Main schema imports
from .user import UserCreate, UserUpdate, UserOut
from .training import TrainingCreate, TrainingUpdate, TrainingOut
from .exercise import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseOut,
    WithWeightCreate,
    WithWeightUpdate,
    WithWeightOut,
    WithoutWeightCreate,
    WithoutWeightUpdate,
    WithoutWeightOut,
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "TrainingCreate",
    "TrainingUpdate",
    "TrainingOut",
    "ExerciseCreate",
    "ExerciseUpdate",
    "ExerciseOut",
    "WithWeightCreate",
    "WithWeightUpdate",
    "WithWeightOut",
    "WithoutWeightCreate",
    "WithoutWeightUpdate",
    "WithoutWeightOut",
]
