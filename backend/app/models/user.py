from sqlalchemy import Column, Integer, String, Float, Date, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class Genero(str, enum.Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"
    NAO_INFORMADO = "nao_informado"


class NivelAtividade(str, enum.Enum):
    SEDENTARIO = "sedentario"
    LEVE = "leve"
    MODERADO = "moderado"
    INTENSO = "intenso"
    MUITO_INTENSO = "muito_intenso"


class ObjetivoFitness(str, enum.Enum):
    PERDA_PESO = "perda_peso"
    GANHO_MASSA = "ganho_massa"
    DEFINICAO = "definicao"
    RESISTENCIA = "resistencia"
    FORCA = "forca"
    SAUDE_GERAL = "saude_geral"


class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    
    # Perfil físico
    data_nascimento = Column(Date, nullable=True)
    genero = Column(Enum(Genero), default=Genero.NAO_INFORMADO)
    altura_cm = Column(Float, nullable=True)
    peso_kg = Column(Float, nullable=True)
    
    # Perfil fitness
    nivel_atividade = Column(Enum(NivelAtividade), default=NivelAtividade.SEDENTARIO)
    objetivo_principal = Column(Enum(ObjetivoFitness), default=ObjetivoFitness.SAUDE_GERAL)
    experiencia_treino_anos = Column(Float, default=0.0)
    
    # Informações adicionais
    bio = Column(Text, nullable=True)
    meta_peso_kg = Column(Float, nullable=True)
    
    # Configurações do app
    is_active = Column(Integer, default=1)
    is_premium = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    treinos = relationship("Treino", back_populates="usuario", cascade="all, delete-orphan")
    historico_exercicios = relationship("HistoricoExecucao", back_populates="usuario", cascade="all, delete-orphan")
    templates_treino = relationship("TemplateTreino", back_populates="criador", cascade="all, delete-orphan")