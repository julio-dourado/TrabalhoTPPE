from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.exercicio import Exercicio, ExercicioCreate, ExercicioUpdate
from ..schemas.usuario import Usuario
from ..crud.exercicio import get_exercicio, get_exercicios_by_treino, create_exercicio, update_exercicio, delete_exercicio
from ..auth.auth import get_current_active_user

router = APIRouter(prefix="/exercicios", tags=["exercicios"], dependencies=[Depends(get_current_active_user)])


@router.post("/treinos/{treino_id}/exercicios", response_model=Exercicio, status_code=status.HTTP_201_CREATED)
def create_new_exercicio(
    treino_id: int,
    exercicio: ExercicioCreate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cria novo exercício em um treino"""
    db_exercicio = create_exercicio(
        db=db, exercicio=exercicio, treino_id=treino_id, usuario_id=current_user.id
    )
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return db_exercicio


@router.get("/treinos/{treino_id}/exercicios", response_model=List[Exercicio])
def read_exercicios_by_treino(
    treino_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Lista exercícios de um treino"""
    exercicios = get_exercicios_by_treino(
        db, treino_id=treino_id, usuario_id=current_user.id, skip=skip, limit=limit
    )
    return exercicios


@router.get("/{exercicio_id}", response_model=Exercicio)
def read_exercicio(
    exercicio_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Busca exercício por ID"""
    db_exercicio = get_exercicio(db, exercicio_id=exercicio_id, usuario_id=current_user.id)
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return db_exercicio


@router.put("/{exercicio_id}", response_model=Exercicio)
def update_exercicio_endpoint(
    exercicio_id: int,
    exercicio: ExercicioUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualiza exercício"""
    db_exercicio = update_exercicio(
        db, exercicio_id=exercicio_id, exercicio=exercicio, usuario_id=current_user.id
    )
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return db_exercicio


@router.delete("/{exercicio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercicio_endpoint(
    exercicio_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove exercício"""
    if not delete_exercicio(db, exercicio_id=exercicio_id, usuario_id=current_user.id):
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return None 