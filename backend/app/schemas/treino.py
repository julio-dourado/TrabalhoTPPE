from pydantic import BaseModel, field_validator
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .exercicio import Exercicio


class TreinoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip()
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip()


class TreinoCreate(TreinoBase):
    pass


class TreinoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None


class TreinoInDB(TreinoBase):
    id: int
    usuario_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Treino(TreinoInDB):
    pass


class TreinoWithExercicios(Treino):
    exercicios: List["Exercicio"] = [] 