from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.usuario import Usuario, UsuarioUpdate
from ..crud.usuario import get_usuario, get_usuarios, update_usuario, delete_usuario
from ..auth.auth import get_current_active_user

router = APIRouter(prefix="/usuarios", tags=["usuarios"], dependencies=[Depends(get_current_active_user)])


@router.get("/", response_model=List[Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista usuários"""
    usuarios = get_usuarios(db, skip=skip, limit=limit)
    return usuarios


@router.get("/me/profile", response_model=Usuario)
def read_my_profile(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna perfil do usuário atual"""
    db_usuario = get_usuario(db, usuario_id=current_user.id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.get("/me/profile-complete")
def read_my_profile_complete(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Retorna perfil completo do usuário atual com treinos"""
    db_usuario = get_usuario(db, usuario_id=current_user.id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Buscar treinos separadamente
    from ..crud.treino import get_treinos_by_usuario
    treinos = get_treinos_by_usuario(db, usuario_id=current_user.id)
    
    return {
        "id": db_usuario.id,
        "nome": db_usuario.nome,
        "email": db_usuario.email,
        "is_active": db_usuario.is_active,
        "created_at": db_usuario.created_at,
        "treinos": treinos
    }


@router.get("/{usuario_id}", response_model=Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Busca usuário por ID"""
    db_usuario = get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario


@router.put("/me", response_model=Usuario)
def update_my_profile(
    usuario: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualiza dados do usuário atual"""
    db_usuario = update_usuario(db, usuario_id=current_user.id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove conta do usuário atual"""
    if not delete_usuario(db, usuario_id=current_user.id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return None 