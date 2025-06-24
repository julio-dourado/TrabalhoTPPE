from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.user import UserOut
from app.schemas.exercise import ExercicioCreate, ExercicioOut, ExercicioSummary
from app.models.training import StatusTreino, CategoriaTreino

class TreinoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255, example="Treino de Pernas")
    descricao: Optional[str] = Field(None, max_length=1000, example="Treino focado em força para membros inferiores")
    categoria: CategoriaTreino = Field(default=CategoriaTreino.FORCA)
    duracao_estimada_min: int = Field(default=60, ge=15, le=300, description="Duração estimada em minutos")

class TreinoCreate(TreinoBase):
    exercicios: List[ExercicioCreate] = Field(..., min_length=1, max_length=20, description="Lista de exercícios do treino")
    model_config = ConfigDict(extra='forbid')

class TreinoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    descricao: Optional[str] = Field(None, max_length=1000)
    categoria: Optional[CategoriaTreino] = None
    duracao_estimada_min: Optional[int] = Field(None, ge=15, le=300)
    status: Optional[StatusTreino] = None
    
    # Campos de execução
    duracao_real_min: Optional[int] = Field(None, ge=1, le=600)
    calorias_queimadas: Optional[float] = Field(None, ge=0, le=2000)
    volume_total_kg: Optional[float] = Field(None, ge=0, le=50000)
    
    # Avaliação
    dificuldade_percebida: Optional[int] = Field(None, ge=1, le=10, description="RPE - Rate of Perceived Exertion")
    satisfacao: Optional[int] = Field(None, ge=1, le=5, description="Nível de satisfação (1-5)")
    observacoes: Optional[str] = Field(None, max_length=1000)
    
    model_config = ConfigDict(extra='forbid')

class TreinoOut(TreinoBase):
    id: int
    usuario_id: int
    status: StatusTreino = StatusTreino.PLANEJADO
    
    # Dados de execução
    duracao_real_min: Optional[int] = None
    calorias_queimadas: Optional[float] = None
    volume_total_kg: Optional[float] = None
    
    # Avaliação
    dificuldade_percebida: Optional[int] = None
    satisfacao: Optional[int] = None
    observacoes: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
    iniciado_em: Optional[datetime] = None
    finalizado_em: Optional[datetime] = None
    
    # Relacionamentos
    exercicios: List[ExercicioOut] = []
    
    model_config = ConfigDict(from_attributes=True)

class TreinoSummary(BaseModel):
    """Resumo do treino para listas"""
    id: int
    nome: str
    categoria: CategoriaTreino
    status: StatusTreino
    duracao_estimada_min: int
    duracao_real_min: Optional[int] = None
    total_exercicios: int
    created_at: datetime
    finalizado_em: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class TreinoIniciar(BaseModel):
    """Schema para iniciar um treino"""
    observacoes_iniciais: Optional[str] = Field(None, max_length=500)

class TreinoFinalizar(BaseModel):
    """Schema para finalizar um treino"""
    duracao_real_min: int = Field(..., gt=0, le=480)
    calorias_queimadas: Optional[float] = Field(None, ge=0, le=2000)
    volume_total_kg: Optional[float] = Field(None, ge=0, le=100000)
    dificuldade_percebida: int = Field(..., ge=1, le=10, description="RPE - Rate of Perceived Exertion")
    satisfacao: int = Field(..., ge=1, le=5, description="Satisfação de 1 a 5 estrelas")
    observacoes: Optional[str] = Field(None, max_length=1000)

# Schemas para Templates de Treino
class TemplateTreinoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255, example="Template Push/Pull/Legs")
    descricao: Optional[str] = Field(None, max_length=1000)
    categoria: CategoriaTreino = Field(default=CategoriaTreino.FORCA)
    nivel_dificuldade: str = Field(default="iniciante", pattern="^(iniciante|intermediario|avancado)$")
    duracao_estimada_min: int = Field(default=60, ge=15, le=300)
    is_publico: bool = Field(default=False, description="Se o template é público para outros usuários")

class ExercicioTemplateCreate(BaseModel):
    exercicio_id: int
    ordem: int = Field(..., ge=1, le=50, description="Ordem do exercício no template")
    series_sugeridas: int = Field(..., gt=0, le=20)
    repeticoes_sugeridas: int = Field(..., gt=0, le=500)
    peso_sugerido_kg: Optional[float] = Field(None, gt=0, le=1000)
    tempo_descanso_seg: int = Field(default=60, ge=0, le=600)
    observacoes: Optional[str] = Field(None, max_length=500)

class ExercicioTemplateOut(ExercicioTemplateCreate):
    id: int
    template_id: int
    exercicio: ExercicioSummary
    model_config = ConfigDict(from_attributes=True)

class TemplateTreinoCreate(TemplateTreinoBase):
    exercicios: List[ExercicioTemplateCreate] = Field(..., min_length=1, max_length=20)
    model_config = ConfigDict(extra='forbid')

class TemplateTreinoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    descricao: Optional[str] = Field(None, max_length=1000)
    categoria: Optional[CategoriaTreino] = None
    nivel_dificuldade: Optional[str] = Field(None, pattern="^(iniciante|intermediario|avancado)$")
    duracao_estimada_min: Optional[int] = Field(None, ge=15, le=300)
    is_publico: Optional[bool] = None
    model_config = ConfigDict(extra='forbid')

class TemplateTreinoOut(TemplateTreinoBase):
    id: int
    criador_id: int
    exercicios: List[ExercicioTemplateOut] = []
    total_exercicios: int
    vezes_usado: int = 0
    avaliacao_media: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class TemplateTreinoSummary(BaseModel):
    """Resumo do template para listas"""
    id: int
    nome: str
    categoria: CategoriaTreino
    nivel_dificuldade: str
    duracao_estimada_min: int
    total_exercicios: int
    vezes_usado: int
    avaliacao_media: Optional[float] = None
    is_publico: bool
    criador_nome: Optional[str] = None  # Nome do criador se for template público
    model_config = ConfigDict(from_attributes=True)

class CriarTreinoDeTemplate(BaseModel):
    """Schema para criar treino a partir de template"""
    template_id: int
    nome_treino: Optional[str] = Field(None, min_length=1, max_length=255)
    observacoes: Optional[str] = Field(None, max_length=500)

# Schemas para Estatísticas
class TreinoStats(BaseModel):
    """Estatísticas de treinos do usuário"""
    total_treinos: int = 0
    treinos_concluidos: int = 0
    treinos_em_andamento: int = 0
    tempo_total_min: int = 0
    calorias_total: float = 0
    volume_total_kg: float = 0
    categoria_favorita: Optional[CategoriaTreino] = None
    streak_atual: int = 0  # Dias consecutivos treinando
    melhor_streak: int = 0

class TreinoFilter(BaseModel):
    """Filtros para busca de treinos"""
    categoria: Optional[CategoriaTreino] = None
    status: Optional[StatusTreino] = None
    nivel_dificuldade: Optional[str] = Field(None, pattern="^(iniciante|intermediario|avancado)$")
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    nome_contains: Optional[str] = Field(None, max_length=100)
    duracao_min: Optional[int] = Field(None, ge=15)
    duracao_max: Optional[int] = Field(None, le=300)

class TemplateFilter(BaseModel):
    """Filtros para busca de templates"""
    categoria: Optional[CategoriaTreino] = None
    nivel_dificuldade: Optional[str] = Field(None, pattern="^(iniciante|intermediario|avancado)$")
    is_publico: Optional[bool] = None
    criador_id: Optional[int] = None
    nome_contains: Optional[str] = Field(None, max_length=100)
