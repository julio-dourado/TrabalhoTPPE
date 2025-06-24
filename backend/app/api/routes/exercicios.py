from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.exercise import ExercicioCreate, ExercicioUpdate, ExercicioOut
from app.services import exercise_service

router = APIRouter(prefix="/exercicios", tags=["Exercícios"])


@router.post(
    "/",
    response_model=ExercicioOut,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo exercício"
)
def create_exercise_route(
    exercicio_data: ExercicioCreate,
    db: Session = Depends(get_db)
):
    """
    US11: Criar exercícios com peso, informando nome, músculo, repetições, sets e carga.
    US14: Criar exercícios sem peso, informando nome, tempo e distância.
    
    Cria um novo exercício com peso ou sem peso baseado no tipo especificado.
    """
    return exercise_service.create_exercise(db=db, exercicio_data=exercicio_data)


@router.get(
    "/",
    response_model=List[ExercicioOut],
    summary="Lista todos os exercícios"
)
def get_exercises_route(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: ComPeso ou SemPeso"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os exercícios ou filtra por tipo específico.
    
    - **tipo**: Opcional. Se fornecido, filtra exercícios por tipo ('ComPeso' ou 'SemPeso')
    """
    if tipo:
        if tipo not in ["ComPeso", "SemPeso"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo deve ser 'ComPeso' ou 'SemPeso'"
            )
        return exercise_service.get_exercises_by_type(db=db, tipo_exercicio=tipo)
    
    return exercise_service.get_all_exercises(db=db)


@router.get(
    "/{exercise_id}",
    response_model=ExercicioOut,
    summary="Obtém um exercício específico por ID"
)
def get_exercise_route(
    exercise_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca um exercício específico pelo seu ID.
    """
    exercicio = exercise_service.get_exercise_by_id(db=db, exercise_id=exercise_id)
    if not exercicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado."
        )
    return exercicio


@router.put(
    "/{exercise_id}",
    response_model=ExercicioOut,
    summary="Atualiza um exercício existente"
)
def update_exercise_route(
    exercise_id: int,
    exercicio_data: ExercicioUpdate,
    db: Session = Depends(get_db)
):
    """
    US12: Editar exercícios com peso.
    US15: Editar exercícios sem peso.
    
    Atualiza um exercício existente. Apenas os campos fornecidos serão atualizados.
    """
    updated_exercicio = exercise_service.update_exercise(
        db=db, 
        exercise_id=exercise_id, 
        exercicio_data=exercicio_data
    )
    if not updated_exercicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado."
        )
    return updated_exercicio


@router.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um exercício"
)
def delete_exercise_route(
    exercise_id: int,
    db: Session = Depends(get_db)
):
    """
    US13: Excluir exercícios com peso.
    US16: Excluir exercícios sem peso.
    
    Remove um exercício do sistema. Se o exercício estiver sendo usado em treinos,
    os vínculos também serão removidos.
    """
    if not exercise_service.delete_exercise(db=db, exercise_id=exercise_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado."
        )


@router.get(
    "/com-peso/",
    response_model=List[ExercicioOut],
    summary="Lista apenas exercícios com peso"
)
def get_weight_exercises_route(db: Session = Depends(get_db)):
    """
    Lista apenas exercícios do tipo 'ComPeso'.
    Útil para interfaces específicas de exercícios com peso.
    """
    return exercise_service.get_exercises_by_type(db=db, tipo_exercicio="ComPeso")


@router.get(
    "/sem-peso/",
    response_model=List[ExercicioOut],
    summary="Lista apenas exercícios cardio"
)
def get_cardio_exercises_route(db: Session = Depends(get_db)):
    """
    Lista apenas exercícios do tipo 'SemPeso'.
    Útil para interfaces específicas de exercícios cardio.
    """
    return exercise_service.get_exercises_by_type(db=db, tipo_exercicio="SemPeso") 