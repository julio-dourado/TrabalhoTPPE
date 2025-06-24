from typing import List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserOut

class ExercicioBase(BaseModel):
    nome: str = Field(..., example="Agachamento")
    serie: int = Field(..., example=3)
    repeticoes: int = Field(..., example=10)
    comentario: Optional[str] = Field(None, example="Focar na forma.")

class ComPesoCreate(BaseModel):
    peso: float = Field(..., example=50.0)

class SemPesoCreate(BaseModel):
    tempo_seg: float = Field(..., example=60.0)
    distancia_m: float = Field(..., example=100.0)
    meta_velocidade: float = Field(..., example=1.6)

class ExercicioCreate(ExercicioBase):
    tipo_exercicio: str = Field(..., pattern="^(ComPeso|SemPeso)$", example="ComPeso")
    com_peso_details: Optional[ComPesoCreate] = None
    sem_peso_details: Optional[SemPesoCreate] = None

    model_config = ConfigDict(extra='forbid')

    def model_post_init(self, __context):
        if self.tipo_exercicio == "ComPeso":
            if not self.com_peso_details:
                raise ValueError("com_peso_details must be provided for 'ComPeso' exercise type.")
            if self.sem_peso_details:
                raise ValueError("sem_peso_details should not be provided for 'ComPeso' exercise type.")
        elif self.tipo_exercicio == "SemPeso":
            if not self.sem_peso_details:
                raise ValueError("sem_peso_details must be provided for 'SemPeso' exercise type.")
            if self.com_peso_details:
                raise ValueError("com_peso_details should not be provided for 'SemPeso' exercise type.")
        else:
            raise ValueError("Invalid tipo_exercicio. Must be 'ComPeso' or 'SemPeso'.")


class ComPesoOut(ComPesoCreate):
    id: int
    exercicio_id: int
    model_config = ConfigDict(from_attributes=True)

class SemPesoOut(SemPesoCreate):
    id: int
    exercicio_id: int
    model_config = ConfigDict(from_attributes=True)

class ExercicioOut(ExercicioBase):
    id: int
    tipo_exercicio: str
    com_peso_details: Optional[ComPesoOut] = None
    sem_peso_details: Optional[SemPesoOut] = None
    model_config = ConfigDict(from_attributes=True)

class TreinoBase(BaseModel):
    nome: str = Field(..., example="Treino de Força Superior")

class TreinoCreate(TreinoBase):
    exercicios: List[ExercicioCreate] = Field(..., min_length=1)

class TreinoUpdate(TreinoBase):
    nome: Optional[str] = None

class TreinoOut(TreinoBase):
    id: int
    usuario: UserOut
    exercicios: List[ExercicioOut] = []

    model_config = ConfigDict(from_attributes=True)
