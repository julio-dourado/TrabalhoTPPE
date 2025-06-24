from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ExercicioBase(BaseModel):
    nome: str = Field(..., min_length=1, example="Agachamento")
    serie: int = Field(..., gt=0, example=3)
    repeticoes: int = Field(..., gt=0, example=10)
    comentario: Optional[str] = Field(None, example="Focar na forma.")


class ComPesoCreate(BaseModel):
    peso: float = Field(..., gt=0, example=50.0)


class SemPesoCreate(BaseModel):
    tempo_seg: float = Field(..., gt=0, example=60.0)
    distancia_m: float = Field(..., ge=0, example=100.0)
    meta_velocidade: float = Field(..., gt=0, example=1.6)


class ComPesoUpdate(BaseModel):
    peso: Optional[float] = Field(None, gt=0, example=50.0)


class SemPesoUpdate(BaseModel):
    tempo_seg: Optional[float] = Field(None, gt=0, example=60.0)
    distancia_m: Optional[float] = Field(None, ge=0, example=100.0)
    meta_velocidade: Optional[float] = Field(None, gt=0, example=1.6)


class ExercicioCreate(ExercicioBase):
    tipo_exercicio: str = Field(..., pattern="^(ComPeso|SemPeso)$", example="ComPeso")
    com_peso_details: Optional[ComPesoCreate] = None
    sem_peso_details: Optional[SemPesoCreate] = None

    model_config = ConfigDict(extra='forbid')

    def model_post_init(self, __context):
        if self.tipo_exercicio == "ComPeso":
            if not self.com_peso_details:
                raise ValueError("com_peso_details deve ser fornecido para exercício 'ComPeso'.")
            if self.sem_peso_details:
                raise ValueError("sem_peso_details não deve ser fornecido para exercício 'ComPeso'.")
        elif self.tipo_exercicio == "SemPeso":
            if not self.sem_peso_details:
                raise ValueError("sem_peso_details deve ser fornecido para exercício 'SemPeso'.")
            if self.com_peso_details:
                raise ValueError("com_peso_details não deve ser fornecido para exercício 'SemPeso'.")
        else:
            raise ValueError("tipo_exercicio inválido. Deve ser 'ComPeso' ou 'SemPeso'.")


class ExercicioUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="Agachamento")
    serie: Optional[int] = Field(None, example=3)
    repeticoes: Optional[int] = Field(None, example=10)
    comentario: Optional[str] = Field(None, example="Focar na forma.")
    com_peso_details: Optional[ComPesoUpdate] = None
    sem_peso_details: Optional[SemPesoUpdate] = None

    model_config = ConfigDict(extra='forbid')


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