from sqlalchemy.orm import Session
from typing import Optional

from ..models.usuario import Usuario
from ..schemas.usuario import UsuarioCreate, UsuarioUpdate
from ..auth.auth import get_password_hash


def get_usuario(db: Session, usuario_id: int) -> Optional[Usuario]:
    """Busca usuário por ID"""
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def get_usuario_by_email(db: Session, email: str) -> Optional[Usuario]:
    """Busca usuário por email"""
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    """Lista usuários com paginação"""
    return db.query(Usuario).offset(skip).limit(limit).all()


def create_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    """Cria novo usuário"""
    hashed_password = get_password_hash(usuario.password)
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        hashed_password=hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate) -> Optional[Usuario]:
    """Atualiza usuário"""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        return None
    
    update_data = usuario.model_dump(exclude_unset=True)
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        update_data["hashed_password"] = hashed_password
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(db_usuario, field, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def delete_usuario(db: Session, usuario_id: int) -> bool:
    """Remove usuário"""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        return False
    
    db.delete(db_usuario)
    db.commit()
    return True 