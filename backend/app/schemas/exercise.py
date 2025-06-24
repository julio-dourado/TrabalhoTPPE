from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from app.models.exercise import GrupoMuscular, Dificuldade, TipoExercicio


class ExercicioBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255, example="Agachamento")
    grupo_muscular: GrupoMuscular = Field(..., example=GrupoMuscular.PERNAS)
    dificuldade: Dificuldade = Field(default=Dificuldade.INICIANTE)
    serie: int = Field(..., gt=0, le=20, example=3)
    repeticoes: int = Field(..., gt=0, le=500, example=10)
    comentario: Optional[str] = Field(None, max_length=500, example="Focar na forma.")
    instrucoes: Optional[str] = Field(None, max_length=2000, example="Mantenha os pés afastados na largura dos ombros...")
    tempo_descanso_seg: int = Field(default=60, ge=0, le=600)
    is_composto: bool = Field(default=False, description="Se é exercício composto (True) ou isolado (False)")
    equipamento: Optional[str] = Field(None, max_length=100, example="Barra olímpica")


class ComPesoCreate(BaseModel):
    peso_kg: float = Field(..., gt=0, le=1000, example=50.0)
    peso_maximo_kg: Optional[float] = Field(None, gt=0, le=1000, example=60.0)
    incremento_sugerido_kg: float = Field(default=2.5, gt=0, le=50)


class SemPesoCreate(BaseModel):
    tempo_seg: Optional[float] = Field(None, gt=0, le=86400, example=60.0)
    distancia_m: Optional[float] = Field(None, ge=0, le=100000, example=100.0)
    calorias_estimadas: Optional[float] = Field(None, ge=0, le=2000, example=50.0)
    intensidade: str = Field(default="moderada", pattern="^(baixa|moderada|alta)$")

    @field_validator('tempo_seg', 'distancia_m')
    @classmethod
    def validate_at_least_one(cls, v, info):
        if not v and not info.data.get('tempo_seg') and not info.data.get('distancia_m'):
            raise ValueError('Pelo menos tempo_seg ou distancia_m deve ser fornecido')
        return v


class ComPesoUpdate(BaseModel):
    peso_kg: Optional[float] = Field(None, gt=0, le=1000, example=50.0)
    peso_maximo_kg: Optional[float] = Field(None, gt=0, le=1000, example=60.0)
    incremento_sugerido_kg: Optional[float] = Field(None, gt=0, le=50)


class SemPesoUpdate(BaseModel):
    tempo_seg: Optional[float] = Field(None, gt=0, le=86400, example=60.0)
    distancia_m: Optional[float] = Field(None, ge=0, le=100000, example=100.0)
    calorias_estimadas: Optional[float] = Field(None, ge=0, le=2000, example=50.0)
    intensidade: Optional[str] = Field(None, pattern="^(baixa|moderada|alta)$")


class ExercicioCreate(ExercicioBase):
    tipo_exercicio: TipoExercicio = Field(..., example=TipoExercicio.COM_PESO)
    com_peso_details: Optional[ComPesoCreate] = None
    sem_peso_details: Optional[SemPesoCreate] = None

    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='after')
    def validate_exercise_details(self):
        if self.tipo_exercicio == TipoExercicio.COM_PESO:
            if not self.com_peso_details:
                raise ValueError("com_peso_details deve ser fornecido para exercício 'COM_PESO'.")
            if self.sem_peso_details:
                raise ValueError("sem_peso_details não deve ser fornecido para exercício 'COM_PESO'.")
        elif self.tipo_exercicio == TipoExercicio.SEM_PESO:
            if not self.sem_peso_details:
                raise ValueError("sem_peso_details deve ser fornecido para exercício 'SEM_PESO'.")
            if self.com_peso_details:
                raise ValueError("com_peso_details não deve ser fornecido para exercício 'SEM_PESO'.")
        return self


class ExercicioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255, example="Agachamento")
    grupo_muscular: Optional[GrupoMuscular] = None
    dificuldade: Optional[Dificuldade] = None
    serie: Optional[int] = Field(None, gt=0, le=20, example=3)
    repeticoes: Optional[int] = Field(None, gt=0, le=500, example=10)
    comentario: Optional[str] = Field(None, max_length=500, example="Focar na forma.")
    instrucoes: Optional[str] = Field(None, max_length=2000)
    tempo_descanso_seg: Optional[int] = Field(None, ge=0, le=600)
    is_composto: Optional[bool] = None
    equipamento: Optional[str] = Field(None, max_length=100)
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
    tipo_exercicio: TipoExercicio
    com_peso_details: Optional[ComPesoOut] = None
    sem_peso_details: Optional[SemPesoOut] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ExercicioSummary(BaseModel):
    """Resumo do exercício para listas"""
    id: int
    nome: str
    grupo_muscular: GrupoMuscular
    tipo_exercicio: TipoExercicio
    dificuldade: Dificuldade
    equipamento: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# Schemas para histórico de execução
class HistoricoExecucaoCreate(BaseModel):
    exercicio_id: int
    treino_id: Optional[int] = None
    series_realizadas: int = Field(..., gt=0, le=50)
    repeticoes_realizadas: int = Field(..., gt=0, le=1000)
    peso_utilizado_kg: Optional[float] = Field(None, gt=0, le=1000)
    tempo_execucao_seg: Optional[float] = Field(None, gt=0, le=86400)
    distancia_realizada_m: Optional[float] = Field(None, ge=0, le=100000)
    dificuldade_percebida: Optional[int] = Field(None, ge=1, le=10, description="RPE - Rate of Perceived Exertion")
    observacoes: Optional[str] = Field(None, max_length=1000)


class HistoricoExecucaoOut(HistoricoExecucaoCreate):
    id: int
    usuario_id: int
    executado_em: datetime
    exercicio: ExercicioSummary
    model_config = ConfigDict(from_attributes=True)


class ExercicioStats(BaseModel):
    """Estatísticas de um exercício específico"""
    exercicio_id: int
    nome_exercicio: str
    total_execucoes: int = 0
    volume_total_kg: float = 0
    melhor_peso_kg: Optional[float] = None
    melhor_repeticoes: Optional[int] = None
    progressao_peso_30d: Optional[float] = None  # % de aumento nos últimos 30 dias
    ultima_execucao: Optional[datetime] = None
    rpe_medio: Optional[float] = None


class ExercicioFilter(BaseModel):
    """Filtros para busca de exercícios"""
    grupo_muscular: Optional[GrupoMuscular] = None
    dificuldade: Optional[Dificuldade] = None
    tipo_exercicio: Optional[TipoExercicio] = None
    equipamento: Optional[str] = None
    is_composto: Optional[bool] = None
    nome_contains: Optional[str] = Field(None, max_length=100) 