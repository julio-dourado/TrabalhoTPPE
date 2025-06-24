from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from datetime import datetime

from app.models.exercise import Exercicio, ComPeso, SemPeso, TipoExercicio
from app.models.training import Treino
from app.schemas.exercise import ExercicioCreate, ExercicioUpdate, ExercicioOut, ComPesoOut, SemPesoOut

def _convert_exercicio_model_to_out_schema(exercicio_model: Exercicio) -> ExercicioOut:
    """Converte modelo de exercício para schema de saída"""
    com_peso_out = None
    sem_peso_out = None
    
    if exercicio_model.tipo_exercicio == TipoExercicio.COM_PESO and exercicio_model.com_peso_details:
        com_peso_out = ComPesoOut.model_validate(exercicio_model.com_peso_details)
    elif exercicio_model.tipo_exercicio == TipoExercicio.SEM_PESO and exercicio_model.sem_peso_details:
        sem_peso_out = SemPesoOut.model_validate(exercicio_model.sem_peso_details)
    
    return ExercicioOut(
        id=exercicio_model.id,
        nome=exercicio_model.nome,
        grupo_muscular=exercicio_model.grupo_muscular,
        dificuldade=exercicio_model.dificuldade,
        serie=exercicio_model.serie,
        repeticoes=exercicio_model.repeticoes,
        comentario=exercicio_model.comentario,
        instrucoes=exercicio_model.instrucoes,
        tempo_descanso_seg=exercicio_model.tempo_descanso_seg,
        is_composto=exercicio_model.is_composto,
        equipamento=exercicio_model.equipamento,
        tipo_exercicio=exercicio_model.tipo_exercicio,
        com_peso_details=com_peso_out,
        sem_peso_details=sem_peso_out,
        created_at=exercicio_model.created_at,
        updated_at=exercicio_model.updated_at
    )

def _create_exercise_details_in_db(db: Session, exercise_obj: Exercicio, exercicio_schema: ExercicioCreate):
    """Cria detalhes específicos do exercício (com peso ou sem peso)"""
    if exercicio_schema.tipo_exercicio == TipoExercicio.COM_PESO and exercicio_schema.com_peso_details:
        com_peso = ComPeso(exercicio_id=exercise_obj.id, **exercicio_schema.com_peso_details.model_dump())
        db.add(com_peso)
        db.flush()
    elif exercicio_schema.tipo_exercicio == TipoExercicio.SEM_PESO and exercicio_schema.sem_peso_details:
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
        grupo_muscular=exercicio_data.grupo_muscular,
        dificuldade=exercicio_data.dificuldade,
        serie=exercicio_data.serie,
        repeticoes=exercicio_data.repeticoes,
        comentario=exercicio_data.comentario,
        instrucoes=exercicio_data.instrucoes,
        tempo_descanso_seg=exercicio_data.tempo_descanso_seg,
        is_composto=exercicio_data.is_composto,
        equipamento=exercicio_data.equipamento,
        tipo_exercicio=exercicio_data.tipo_exercicio,
        created_at=datetime.utcnow()
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
    Lista exercícios por tipo (COM_PESO ou SEM_PESO)
    """
    if tipo_exercicio not in ["COM_PESO", "SEM_PESO"]:
        return []
    
    tipo_enum = TipoExercicio.COM_PESO if tipo_exercicio == "COM_PESO" else TipoExercicio.SEM_PESO
    
    exercicios = db.execute(
        select(Exercicio)
        .where(Exercicio.tipo_exercicio == tipo_enum)
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
    update_fields = exercicio_data.model_dump(exclude_unset=True, exclude={'com_peso_details', 'sem_peso_details'})
    for field, value in update_fields.items():
        setattr(exercicio, field, value)
    
    exercicio.updated_at = datetime.utcnow()

    # Atualiza detalhes específicos baseado no tipo
    if exercicio.tipo_exercicio == TipoExercicio.COM_PESO and exercicio_data.com_peso_details is not None and exercicio.com_peso_details:
        for field, value in exercicio_data.com_peso_details.model_dump(exclude_unset=True).items():
            setattr(exercicio.com_peso_details, field, value)
    elif exercicio.tipo_exercicio == TipoExercicio.SEM_PESO and exercicio_data.sem_peso_details is not None and exercicio.sem_peso_details:
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