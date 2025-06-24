from typing import List, Optional, Union
from sqlmodel import Field, Relationship, SQLModel 
from sqlalchemy.orm import relationship
from app.models.user import User as SQLAlchemyUser


class TreinoExercicioLink(SQLModel, table=True):
    treino_id: Optional[int] = Field(default=None, foreign_key="treino.id", primary_key=True)
    exercicio_id: Optional[int] = Field(default=None, foreign_key="exercicio.id", primary_key=True)


class ComPeso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercicio_id: int = Field(foreign_key="exercicio.id", unique=True)
    peso: float

    exercicio: "Exercicio" = Relationship(back_populates="com_peso_details")

class SemPeso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercicio_id: int = Field(foreign_key="exercicio.id", unique=True)
    tempo_seg: float
    distancia_m: float
    meta_velocidade: float

    exercicio: "Exercicio" = Relationship(back_populates="sem_peso_details")


class Exercicio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    serie: int
    repeticoes: int
    comentario: Optional[str] = None
    tipo_exercicio: str

    com_peso_details: Optional[ComPeso] = Relationship(back_populates="exercicio")
    sem_peso_details: Optional[SemPeso] = Relationship(back_populates="exercicio")

    treinos: List["Treino"] = Relationship(back_populates="exercicios", link_model=TreinoExercicioLink)


class Treino(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    usuario_id: int = Field(foreign_key="usuarios.id")

    usuario: Optional[SQLAlchemyUser] = Relationship(sa_relationship_args={"lazy": "joined"})

    exercicios: List[Exercicio] = Relationship(back_populates="treinos", link_model=TreinoExercicioLink)

