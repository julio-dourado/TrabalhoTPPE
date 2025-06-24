from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.models.exercise import Exercicio, ComPeso, SemPeso
from app.models.training import Treino
from app.schemas.exercise import ExercicioCreate, ExercicioUpdate, ExercicioOut, ComPesoOut, SemPesoOut

def _convert_exercicio_model_to_out_schema(exercicio_model: Exercicio) -> ExercicioOut:
    """Converte modelo de exercício para schema de saída"""
    com_peso_out = None
    sem_peso_out = None
    
    if exercicio_model.tipo_exercicio == "ComPeso" and exercicio_model.com_peso_details:
        com_peso_out = ComPesoOut.model_validate(exercicio_model.com_peso_details)
    elif exercicio_model.tipo_exercicio == "SemPeso" and exercicio_model.sem_peso_details:
        sem_peso_out = SemPesoOut.model_validate(exercicio_model.sem_peso_details)
    
    return ExercicioOut(
        id=exercicio_model.id,
        nome=exercicio_model.nome,
        serie=exercicio_model.serie,
        repeticoes=exercicio_model.repeticoes,
        comentario=exercicio_model.comentario,
        tipo_exercicio=exercicio_model.tipo_exercicio,
        com_peso_details=com_peso_out,
        sem_peso_details=sem_peso_out
    )

def _create_exercise_details_in_db(db: Session, exercise_obj: Exercicio, exercicio_schema: ExercicioCreate):
    """Cria detalhes específicos do exercício (com peso ou sem peso)"""
    if exercicio_schema.tipo_exercicio == "ComPeso" and exercicio_schema.com_peso_details:
        com_peso = ComPeso(exercicio_id=exercise_obj.id, **exercicio_schema.com_peso_details.model_dump())
        db.add(com_peso)
        db.flush()
    elif exercicio_schema.tipo_exercicio == "SemPeso" and exercicio_schema.sem_peso_details:
        sem_peso = SemPeso(exercicio_id=exercise_obj.id, **exercicio_schema.sem_peso_details.model_dump())
        db.add(sem_peso)
        db.flush()

def create_exercise(db: Session, exercicio_data: ExercicioCreate) -> ExercicioOut:
    """
    US11/US14: Cria um exercício com peso ou sem peso
    """
    # Cria o exercício base
    db_exercicio = Exercicio(
        nome=exercicio_data.nome,
        serie=exercicio_data.serie,
        repeticoes=exercicio_data.repeticoes,
        comentario=exercicio_data.comentario,
        tipo_exercicio=exercicio_data.tipo_exercicio
    )
    db.add(db_exercicio)
    db.flush()

    # Cria os detalhes específicos
    _create_exercise_details_in_db(db, db_exercicio, exercicio_data)
    
    db.commit()
    db.refresh(db_exercicio)

    return _convert_exercicio_model_to_out_schema(db_exercicio)

def get_exercise_by_id(db: Session, exercise_id: int) -> Optional[ExercicioOut]:
    """
    Busca um exercício por ID
    """
    exercicio = db.execute(
        select(Exercicio)
        .where(Exercicio.id == exercise_id)
        .options(
            selectinload(Exercicio.com_peso_details),
            selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().first()

    if not exercicio:
        return None
    
    return _convert_exercicio_model_to_out_schema(exercicio)

def get_exercises_by_type(db: Session, tipo_exercicio: str) -> List[ExercicioOut]:
    """
    Lista exercícios por tipo (ComPeso ou SemPeso)
    """
    if tipo_exercicio not in ["ComPeso", "SemPeso"]:
        return []
    
    exercicios = db.execute(
        select(Exercicio)
        .where(Exercicio.tipo_exercicio == tipo_exercicio)
        .options(
            selectinload(Exercicio.com_peso_details),
            selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().all()

    return [_convert_exercicio_model_to_out_schema(exercicio) for exercicio in exercicios]

def get_all_exercises(db: Session) -> List[ExercicioOut]:
    """
    Lista todos os exercícios
    """
    exercicios = db.execute(
        select(Exercicio)
        .options(
            selectinload(Exercicio.com_peso_details),
            selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().all()

    return [_convert_exercicio_model_to_out_schema(e) for e in exercicios]

def update_exercise(db: Session, exercise_id: int, exercicio_data: ExercicioUpdate) -> Optional[ExercicioOut]:
    """
    US12/US15: Atualiza um exercício existente
    """
    exercicio = db.execute(
        select(Exercicio)
        .where(Exercicio.id == exercise_id)
        .options(
            selectinload(Exercicio.com_peso_details),
            selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().first()

    if not exercicio:
        return None

    # Atualiza campos básicos se fornecidos
    if exercicio_data.nome is not None:
        exercicio.nome = exercicio_data.nome
    if exercicio_data.serie is not None:
        exercicio.serie = exercicio_data.serie
    if exercicio_data.repeticoes is not None:
        exercicio.repeticoes = exercicio_data.repeticoes
    if exercicio_data.comentario is not None:
        exercicio.comentario = exercicio_data.comentario

    # Atualiza detalhes específicos baseado no tipo
    if exercicio.tipo_exercicio == "ComPeso" and exercicio_data.com_peso_details is not None and exercicio.com_peso_details:
        for field, value in exercicio_data.com_peso_details.model_dump(exclude_unset=True).items():
            setattr(exercicio.com_peso_details, field, value)
    elif exercicio.tipo_exercicio == "SemPeso" and exercicio_data.sem_peso_details is not None and exercicio.sem_peso_details:
        for field, value in exercicio_data.sem_peso_details.model_dump(exclude_unset=True).items():
            setattr(exercicio.sem_peso_details, field, value)

    db.add(exercicio)
    db.commit()
    db.refresh(exercicio)

    return _convert_exercicio_model_to_out_schema(exercicio)

def delete_exercise(db: Session, exercise_id: int) -> bool:
    """
    US13/US16: Deleta um exercício
    """
    exercicio = db.execute(
        select(Exercicio)
        .where(Exercicio.id == exercise_id)
    ).scalars().first()

    if not exercicio:
        return False

    # Remove detalhes específicos (cascade deve cuidar disso, mas vamos ser explícitos)
    if exercicio.com_peso_details:
        db.delete(exercicio.com_peso_details)
    if exercicio.sem_peso_details:
        db.delete(exercicio.sem_peso_details)

    # Remove o exercício
    db.delete(exercicio)
    db.commit()
    return True

def get_exercises_in_training(db: Session, training_id: int) -> List[ExercicioOut]:
    """
    Busca exercícios de um treino específico
    """
    treino = db.execute(
        select(Treino)
        .where(Treino.id == training_id)
        .options(
            selectinload(Treino.exercicios).selectinload(Exercicio.com_peso_details),
            selectinload(Treino.exercicios).selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().first()

    if not treino:
        return []

    return [_convert_exercicio_model_to_out_schema(exercicio) for exercicio in treino.exercicios] 