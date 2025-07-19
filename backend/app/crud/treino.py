from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.treino import Treino
from ..schemas.treino import TreinoCreate, TreinoUpdate


def get_treino(db: Session, treino_id: int, usuario_id: int) -> Optional[Treino]:
    """Busca treino por ID do usuário específico"""
    return db.query(Treino).filter(
        Treino.id == treino_id, 
        Treino.usuario_id == usuario_id
    ).first()


def get_treinos_by_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Treino]:
    """Lista treinos de um usuário"""
    return db.query(Treino).filter(
        Treino.usuario_id == usuario_id
    ).offset(skip).limit(limit).all()


def create_treino(db: Session, treino: TreinoCreate, usuario_id: int) -> Treino:
    """Cria novo treino"""
    db_treino = Treino(
        nome=treino.nome,
        descricao=treino.descricao,
        usuario_id=usuario_id
    )
    db.add(db_treino)
    db.commit()
    db.refresh(db_treino)
    return db_treino


def update_treino(db: Session, treino_id: int, treino: TreinoUpdate, usuario_id: int) -> Optional[Treino]:
    """Atualiza treino"""
    db_treino = db.query(Treino).filter(
        Treino.id == treino_id,
        Treino.usuario_id == usuario_id
    ).first()
    
    if not db_treino:
        return None
    
    update_data = treino.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_treino, field, value)
    
    db.commit()
    db.refresh(db_treino)
    return db_treino


def delete_treino(db: Session, treino_id: int, usuario_id: int) -> bool:
    """Remove treino"""
    db_treino = db.query(Treino).filter(
        Treino.id == treino_id,
        Treino.usuario_id == usuario_id
    ).first()
    
    if not db_treino:
        return False
    
    db.delete(db_treino)
    db.commit()
    return True 