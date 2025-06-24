from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

treino_exercicio_link = Table(
    'treinoexerciciolink',
    Base.metadata,
    Column('treino_id', Integer, ForeignKey('treino.id'), primary_key=True),
    Column('exercicio_id', Integer, ForeignKey('exercicio.id'), primary_key=True)
)

class Treino(Base):
    __tablename__ = 'treino'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("User", back_populates="treinos")
    exercicios = relationship("Exercicio", secondary=treino_exercicio_link, back_populates="treinos")

