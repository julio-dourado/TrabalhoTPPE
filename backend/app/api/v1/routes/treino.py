from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.training import TreinoCreate, TreinoUpdate, TreinoOut
from app.models.user import User as SQLAlchemyUser
from app.api.v1.deps import get_current_user
from app.services import training_service

router = APIRouter(prefix="/treinos", tags=["Treinos"])

@router.post(
    "/",
    response_model=TreinoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo treino para o usuário autenticado"
)
def create_training_route(
    treino_data: TreinoCreate,
    current_user: SQLAlchemyUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return training_service.create_training(db=db, treino_data=treino_data, current_user_id=current_user.id)


@router.get(
    "/",
    response_model=List[TreinoOut],
    summary="Lista todos os treinos do usuário autenticado"
)
def read_trainings_route(
    current_user: SQLAlchemyUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return training_service.get_trainings_for_user(db=db, user_id=current_user.id)


@router.get(
    "/{training_id}",
    response_model=TreinoOut,
    summary="Obtém um treino específico por ID"
)
def read_training_route(
    training_id: int,
    current_user: SQLAlchemyUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    treino = training_service.get_training_by_id_for_user(db=db, training_id=training_id, user_id=current_user.id)
    if not treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino não encontrado ou você não tem permissão para acessá-lo."
        )
    return treino


@router.put(
    "/{training_id}",
    response_model=TreinoOut,
    summary="Atualiza um treino existente"
)
def update_training_route(
    training_id: int,
    treino_data: TreinoUpdate,
    current_user: SQLAlchemyUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_treino = training_service.update_training(db=db, training_id=training_id, user_id=current_user.id, treino_data=treino_data)
    if not updated_treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino não encontrado ou você não tem permissão para atualizá-lo."
        )
    return updated_treino

@router.delete(
    "/{training_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um treino"
)
def delete_training_route(
    training_id: int,
    current_user: SQLAlchemyUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not training_service.delete_training(db=db, training_id=training_id, user_id=current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Treino não encontrado ou você não tem permissão para deletá-lo."
        )
    return

