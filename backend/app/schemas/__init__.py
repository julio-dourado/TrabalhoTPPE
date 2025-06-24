# Importações dos schemas principais
from .user import UserCreate, UserUpdate, UserOut
from .training import TreinoCreate, TreinoUpdate, TreinoOut
from .exercise import (
    ExercicioCreate, 
    ExercicioUpdate, 
    ExercicioOut,
    ComPesoCreate,
    ComPesoUpdate,
    ComPesoOut,
    SemPesoCreate,
    SemPesoUpdate,
    SemPesoOut
)

__all__ = [
    "UserCreate",
    "UserUpdate", 
    "UserOut",
    "TreinoCreate",
    "TreinoUpdate",
    "TreinoOut",
    "ExercicioCreate",
    "ExercicioUpdate",
    "ExercicioOut",
    "ComPesoCreate",
    "ComPesoUpdate",
    "ComPesoOut",
    "SemPesoCreate",
    "SemPesoUpdate",
    "SemPesoOut"
] 