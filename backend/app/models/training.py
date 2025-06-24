from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Text, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class StatusTreino(str, enum.Enum):
    PLANEJADO = "PLANEJADO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"
    PAUSADO = "PAUSADO"
    CANCELADO = "CANCELADO"


class CategoriaTreino(str, enum.Enum):
    FORCA = "FORCA"
    CARDIO = "CARDIO"
    HIIT = "HIIT"
    FUNCIONAL = "FUNCIONAL"
    FLEXIBILIDADE = "FLEXIBILIDADE"
    POWERLIFTING = "POWERLIFTING"
    BODYBUILDING = "BODYBUILDING"
    CROSSFIT = "CROSSFIT"
    YOGA = "YOGA"
    PILATES = "PILATES"


treino_exercicio_link = Table(
    'treino_exercicio',
    Base.metadata,
    Column('treino_id', Integer, ForeignKey('treinos.id'), primary_key=True),
    Column('exercicio_id', Integer, ForeignKey('exercicios.id'), primary_key=True)
)


class Treino(Base):
    __tablename__ = 'treinos'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    descricao = Column(Text, nullable=True)
    categoria = Column(Enum(CategoriaTreino), default=CategoriaTreino.FORCA)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Status e controle
    status = Column(Enum(StatusTreino), default=StatusTreino.PLANEJADO)
    duracao_estimada_min = Column(Integer, default=60)
    duracao_real_min = Column(Integer, nullable=True)
    
    # Estatísticas
    calorias_queimadas = Column(Float, nullable=True)
    volume_total_kg = Column(Float, nullable=True)  # Peso total levantado
    
    # Avaliação
    dificuldade_percebida = Column(Integer, nullable=True)  # 1-10 (RPE)
    satisfacao = Column(Integer, nullable=True)  # 1-5 estrelas
    observacoes = Column(Text, nullable=True)
    
    # Timestamps
    iniciado_em = Column(DateTime(timezone=True), nullable=True)
    finalizado_em = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    usuario = relationship("User", back_populates="treinos")
    exercicios = relationship("Exercicio", secondary=treino_exercicio_link, back_populates="treinos")
    historico_execucoes = relationship("HistoricoExecucao", back_populates="treino", cascade="all, delete-orphan")


class TemplateTreino(Base):
    __tablename__ = 'template_treino'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    descricao = Column(Text, nullable=True)
    categoria = Column(Enum(CategoriaTreino), default=CategoriaTreino.FORCA)
    criador_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Configurações do template
    is_publico = Column(Boolean, default=False)  # False = privado, True = público
    duracao_estimada_min = Column(Integer, default=60)
    nivel_dificuldade = Column(String(20), default="iniciante")
    
    # Estatísticas de uso
    vezes_usado = Column(Integer, default=0)
    avaliacao_media = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    criador = relationship("User", back_populates="templates_treino")
    exercicios_template = relationship("ExercicioTemplate", back_populates="template", cascade="all, delete-orphan")


class ExercicioTemplate(Base):
    __tablename__ = 'exercicio_template'
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey('template_treino.id'), nullable=False)
    exercicio_id = Column(Integer, ForeignKey('exercicios.id'), nullable=False)
    
    # Configurações específicas do exercício no template
    ordem = Column(Integer, nullable=False)  # Ordem de execução
    series_sugeridas = Column(Integer, nullable=False)
    repeticoes_sugeridas = Column(Integer, nullable=False)
    peso_sugerido_kg = Column(Float, nullable=True)
    tempo_descanso_seg = Column(Integer, default=60)
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    template = relationship("TemplateTreino", back_populates="exercicios_template")
    exercicio = relationship("Exercicio")

