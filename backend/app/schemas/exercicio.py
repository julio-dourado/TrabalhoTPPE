from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from ..models.exercicio import TipoExercicio


class ExercicioBase(BaseModel):
    nome: str
    tipo: TipoExercicio
    musculo: Optional[str] = None
    
    # Campos para exercícios com peso
    repeticoes: Optional[int] = None
    sets: Optional[int] = None
    carga: Optional[float] = None
    
    # Campos para exercícios sem peso
    tempo: Optional[int] = None  # em segundos
    distancia: Optional[float] = None  # em metros/km
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip()


class ExercicioCreate(ExercicioBase):
    pass


class ExercicioUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[TipoExercicio] = None
    musculo: Optional[str] = None
    repeticoes: Optional[int] = None
    sets: Optional[int] = None
    carga: Optional[float] = None
    tempo: Optional[int] = None
    distancia: Optional[float] = None


class ExercicioInDB(ExercicioBase):
    id: int
    treino_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Exercicio(ExercicioInDB):
    pass 