from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.treino import Treino, TreinoCreate, TreinoUpdate
from ..schemas.usuario import Usuario
from ..crud.treino import get_treino, get_treinos_by_usuario, create_treino, update_treino, delete_treino
from ..auth.auth import get_current_active_user

router = APIRouter(prefix="/treinos", tags=["treinos"], dependencies=[Depends(get_current_active_user)])


@router.post("/", response_model=Treino, status_code=status.HTTP_201_CREATED)
def create_new_treino(
    treino: TreinoCreate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cria novo treino"""
    return create_treino(db=db, treino=treino, usuario_id=current_user.id)


@router.get("/", response_model=List[Treino])
def read_my_treinos(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Lista treinos do usuário atual"""
    treinos = get_treinos_by_usuario(db, usuario_id=current_user.id, skip=skip, limit=limit)
    return treinos


@router.get("/{treino_id}", response_model=Treino)
def read_treino(
    treino_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Busca treino por ID"""
    db_treino = get_treino(db, treino_id=treino_id, usuario_id=current_user.id)
    if db_treino is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return db_treino

@router.get("/{treino_id}/with-exercicios")
def read_treino_with_exercicios(
    treino_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Busca treino por ID com lista de exercícios"""
    db_treino = get_treino(db, treino_id=treino_id, usuario_id=current_user.id)
    if db_treino is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    # Buscar exercícios separadamente
    from ..crud.exercicio import get_exercicios_by_treino
    exercicios = get_exercicios_by_treino(db, treino_id=treino_id, usuario_id=current_user.id)
    
    return {
        "id": db_treino.id,
        "nome": db_treino.nome,
        "descricao": db_treino.descricao,
        "created_at": db_treino.created_at,
        "usuario_id": db_treino.usuario_id,
        "exercicios": exercicios
    }


@router.put("/{treino_id}", response_model=Treino)
def update_treino_endpoint(
    treino_id: int,
    treino: TreinoUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualiza treino"""
    db_treino = update_treino(db, treino_id=treino_id, treino=treino, usuario_id=current_user.id)
    if db_treino is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return db_treino


@router.delete("/{treino_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_treino_endpoint(
    treino_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove treino"""
    if not delete_treino(db, treino_id=treino_id, usuario_id=current_user.id):
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return None 