from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserOut
from app.schemas.exercise import ExercicioCreate, ExercicioOut

class TreinoBase(BaseModel):
    nome: str = Field(..., min_length=1, example="Treino de Força Superior")

class TreinoCreate(TreinoBase):
    exercicios: List[ExercicioCreate] = Field(..., min_length=1)

class TreinoUpdate(TreinoBase):
    nome: Optional[str] = None

class TreinoOut(TreinoBase):
    id: int
    usuario: UserOut
    exercicios: List[ExercicioOut] = []

    model_config = ConfigDict(from_attributes=True)
