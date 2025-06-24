from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import Genero, NivelAtividade, ObjetivoFitness


class UserBase(BaseModel):
    email: EmailStr
    nome: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    senha: str = Field(..., min_length=6, description="A senha do usuário")


class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=6, description="A nova senha do usuário")
    
    # Perfil físico
    data_nascimento: Optional[date] = None
    genero: Optional[Genero] = None
    altura_cm: Optional[float] = Field(None, gt=0, le=300)
    peso_kg: Optional[float] = Field(None, gt=0, le=500)
    
    # Perfil fitness
    nivel_atividade: Optional[NivelAtividade] = None
    objetivo_principal: Optional[ObjetivoFitness] = None
    experiencia_treino_anos: Optional[float] = Field(None, ge=0, le=50)
    
    # Informações adicionais
    bio: Optional[str] = Field(None, max_length=500)
    meta_peso_kg: Optional[float] = Field(None, gt=0, le=500)


class UserProfileUpdate(BaseModel):
    """Schema específico para atualização de perfil (sem senha)"""
    nome: Optional[str] = Field(None, min_length=2, max_length=255)
    data_nascimento: Optional[date] = None
    genero: Optional[Genero] = None
    altura_cm: Optional[float] = Field(None, gt=0, le=300)
    peso_kg: Optional[float] = Field(None, gt=0, le=500)
    nivel_atividade: Optional[NivelAtividade] = None
    objetivo_principal: Optional[ObjetivoFitness] = None
    experiencia_treino_anos: Optional[float] = Field(None, ge=0, le=50)
    bio: Optional[str] = Field(None, max_length=500)
    meta_peso_kg: Optional[float] = Field(None, gt=0, le=500)


class UserOut(UserBase):
    id: int
    
    # Perfil físico
    data_nascimento: Optional[date] = None
    genero: Optional[Genero] = None
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    
    # Perfil fitness
    nivel_atividade: Optional[NivelAtividade] = None
    objetivo_principal: Optional[ObjetivoFitness] = None
    experiencia_treino_anos: Optional[float] = None
    
    # Informações adicionais
    bio: Optional[str] = None
    meta_peso_kg: Optional[float] = None
    
    # Status
    is_active: bool
    is_premium: bool
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserStats(BaseModel):
    """Estatísticas do usuário para dashboard"""
    total_treinos: int = 0
    treinos_concluidos: int = 0
    treinos_mes_atual: int = 0
    tempo_total_treino_min: int = 0
    calorias_queimadas_total: float = 0
    volume_total_levantado_kg: float = 0
    exercicio_favorito: Optional[str] = None
    streak_atual_dias: int = 0
    maior_streak_dias: int = 0


class UserPublicProfile(BaseModel):
    """Perfil público do usuário (para compartilhamento)"""
    id: int
    nome: str
    bio: Optional[str] = None
    objetivo_principal: Optional[ObjetivoFitness] = None
    experiencia_treino_anos: Optional[float] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)