from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum


class TipoExercicio(enum.Enum):
    COM_PESO = "com_peso"
    SEM_PESO = "sem_peso"


class Exercicio(Base):
    __tablename__ = "exercicios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(Enum(TipoExercicio), nullable=False)
    musculo = Column(String, nullable=True)  # Para exercícios com peso
    
    # Campos para exercícios com peso
    repeticoes = Column(Integer, nullable=True)
    sets = Column(Integer, nullable=True)
    carga = Column(Float, nullable=True)
    
    # Campos para exercícios sem peso
    tempo = Column(Integer, nullable=True)  # em segundos
    distancia = Column(Float, nullable=True)  # em metros/km
    
    treino_id = Column(Integer, ForeignKey("treinos.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    treino = relationship("Treino", back_populates="exercicios") 