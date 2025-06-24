from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class ComPeso(Base):
    __tablename__ = 'compeso'
    
    id = Column(Integer, primary_key=True, index=True)
    exercicio_id = Column(Integer, ForeignKey("exercicio.id"), unique=True, nullable=False)
    peso = Column(Float, nullable=False)

    exercicio = relationship("Exercicio", back_populates="com_peso_details")


class SemPeso(Base):
    __tablename__ = 'sempeso'
    
    id = Column(Integer, primary_key=True, index=True)
    exercicio_id = Column(Integer, ForeignKey("exercicio.id"), unique=True, nullable=False)
    tempo_seg = Column(Float, nullable=False)
    distancia_m = Column(Float, nullable=False)
    meta_velocidade = Column(Float, nullable=False)

    exercicio = relationship("Exercicio", back_populates="sem_peso_details")


class Exercicio(Base):
    __tablename__ = 'exercicio'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    serie = Column(Integer, nullable=False)
    repeticoes = Column(Integer, nullable=False)
    comentario = Column(String(500), nullable=True)
    tipo_exercicio = Column(String(50), nullable=False)

    com_peso_details = relationship("ComPeso", back_populates="exercicio", uselist=False)
    sem_peso_details = relationship("SemPeso", back_populates="exercicio", uselist=False)
    treinos = relationship("Treino", secondary="treinoexerciciolink", back_populates="exercicios") 