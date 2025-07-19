from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .treino import Treino


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip()


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UsuarioInDB(UsuarioBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Usuario(UsuarioInDB):
    pass


class UsuarioWithTreinos(Usuario):
    treinos: List["Treino"] = []


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None 