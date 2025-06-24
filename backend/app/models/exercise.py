from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class GrupoMuscular(str, enum.Enum):
    PEITO = "PEITO"
    COSTAS = "COSTAS"
    OMBROS = "OMBROS"
    BICEPS = "BICEPS"
    TRICEPS = "TRICEPS"
    PERNAS = "PERNAS"
    GLUTEOS = "GLUTEOS"
    ABDOMEN = "ABDOMEN"
    PANTURRILHA = "PANTURRILHA"
    ANTEBRACO = "ANTEBRACO"
    CARDIO = "CARDIO"
    CORPO_INTEIRO = "CORPO_INTEIRO"


class Dificuldade(str, enum.Enum):
    INICIANTE = "INICIANTE"
    INTERMEDIARIO = "INTERMEDIARIO"
    AVANCADO = "AVANCADO"


class TipoExercicio(str, enum.Enum):
    COM_PESO = "COM_PESO"
    SEM_PESO = "SEM_PESO"


class ComPeso(Base):
    __tablename__ = 'com_peso'
    
    id = Column(Integer, primary_key=True, index=True)
    exercicio_id = Column(Integer, ForeignKey("exercicios.id"), unique=True, nullable=False)
    peso_kg = Column(Float, nullable=False)
    # Campos adicionais para progressão
    peso_maximo_kg = Column(Float, nullable=True)  # 1RM estimado
    incremento_sugerido_kg = Column(Float, default=2.5)  # Incremento sugerido para progressão

    exercicio = relationship("Exercicio", back_populates="com_peso_details")


class SemPeso(Base):
    __tablename__ = 'sem_peso'
    
    id = Column(Integer, primary_key=True, index=True)
    exercicio_id = Column(Integer, ForeignKey("exercicios.id"), unique=True, nullable=False)
    tempo_seg = Column(Float, nullable=True)  # Para exercícios baseados em tempo
    distancia_m = Column(Float, nullable=True)  # Para exercícios baseados em distância
    calorias_estimadas = Column(Float, nullable=True)  # Estimativa de calorias
    intensidade = Column(String(20), default="moderada")  # baixa, moderada, alta

    exercicio = relationship("Exercicio", back_populates="sem_peso_details")


class Exercicio(Base):
    __tablename__ = 'exercicios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    grupo_muscular = Column(Enum(GrupoMuscular), nullable=False)
    dificuldade = Column(Enum(Dificuldade), default=Dificuldade.INICIANTE)
    serie = Column(Integer, nullable=False)
    repeticoes = Column(Integer, nullable=False)
    comentario = Column(String(500), nullable=True)
    instrucoes = Column(Text, nullable=True)  # Instruções detalhadas de execução
    tipo_exercicio = Column(Enum(TipoExercicio), nullable=False)
    
    # Campos para melhor experiência do usuário
    tempo_descanso_seg = Column(Integer, default=60)  # Tempo de descanso sugerido
    is_composto = Column(Boolean, default=False)  # Se é exercício composto ou isolado
    equipamento = Column(String(100), nullable=True)  # Equipamento necessário
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    com_peso_details = relationship("ComPeso", back_populates="exercicio", uselist=False, cascade="all, delete-orphan")
    sem_peso_details = relationship("SemPeso", back_populates="exercicio", uselist=False, cascade="all, delete-orphan")
    treinos = relationship("Treino", secondary="treino_exercicio", back_populates="exercicios")
    historico_execucoes = relationship("HistoricoExecucao", back_populates="exercicio", cascade="all, delete-orphan")


# Nova tabela para histórico de execuções
class HistoricoExecucao(Base):
    __tablename__ = 'historico_execucao'
    
    id = Column(Integer, primary_key=True, index=True)
    exercicio_id = Column(Integer, ForeignKey('exercicios.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    treino_id = Column(Integer, ForeignKey('treinos.id'), nullable=True)
    
    # Dados da execução
    series_realizadas = Column(Integer, nullable=False)
    repeticoes_realizadas = Column(Integer, nullable=False)
    peso_utilizado_kg = Column(Float, nullable=True)
    tempo_execucao_seg = Column(Float, nullable=True)
    distancia_realizada_m = Column(Float, nullable=True)
    
    # Avaliação da execução
    dificuldade_percebida = Column(Integer, nullable=True)  # 1-10 (RPE)
    observacoes = Column(Text, nullable=True)
    
    # Timestamp
    executado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    exercicio = relationship("Exercicio", back_populates="historico_execucoes")
    usuario = relationship("User", back_populates="historico_exercicios")
    treino = relationship("Treino", back_populates="historico_execucoes") 