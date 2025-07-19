from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.exercicio import Exercicio
from ..models.treino import Treino
from ..schemas.exercicio import ExercicioCreate, ExercicioUpdate


def get_exercicio(db: Session, exercicio_id: int, usuario_id: int) -> Optional[Exercicio]:
    """Busca exercício por ID verificando se pertence ao usuário"""
    return db.query(Exercicio).join(Treino).filter(
        Exercicio.id == exercicio_id,
        Treino.usuario_id == usuario_id
    ).first()


def get_exercicios_by_treino(db: Session, treino_id: int, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Exercicio]:
    """Lista exercícios de um treino"""
    return db.query(Exercicio).join(Treino).filter(
        Exercicio.treino_id == treino_id,
        Treino.usuario_id == usuario_id
    ).offset(skip).limit(limit).all()


def create_exercicio(db: Session, exercicio: ExercicioCreate, treino_id: int, usuario_id: int) -> Optional[Exercicio]:
    """Cria novo exercício"""
    # Verifica se o treino pertence ao usuário
    treino = db.query(Treino).filter(
        Treino.id == treino_id,
        Treino.usuario_id == usuario_id
    ).first()
    
    if not treino:
        return None
    
    db_exercicio = Exercicio(
        nome=exercicio.nome,
        tipo=exercicio.tipo,
        musculo=exercicio.musculo,
        repeticoes=exercicio.repeticoes,
        sets=exercicio.sets,
        carga=exercicio.carga,
        tempo=exercicio.tempo,
        distancia=exercicio.distancia,
        treino_id=treino_id
    )
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio


def update_exercicio(db: Session, exercicio_id: int, exercicio: ExercicioUpdate, usuario_id: int) -> Optional[Exercicio]:
    """Atualiza exercício"""
    db_exercicio = db.query(Exercicio).join(Treino).filter(
        Exercicio.id == exercicio_id,
        Treino.usuario_id == usuario_id
    ).first()
    
    if not db_exercicio:
        return None
    
    update_data = exercicio.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exercicio, field, value)
    
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio


def delete_exercicio(db: Session, exercicio_id: int, usuario_id: int) -> bool:
    """Remove exercício"""
    db_exercicio = db.query(Exercicio).join(Treino).filter(
        Exercicio.id == exercicio_id,
        Treino.usuario_id == usuario_id
    ).first()
    
    if not db_exercicio:
        return False
    
    db.delete(db_exercicio)
    db.commit()
    return True 