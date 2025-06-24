from typing import List, Optional
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

from app.models.training import Treino, Exercicio, ComPeso, SemPeso, TreinoExercicioLink
from app.models.user import User as SQLAlchemyUser
from app.schemas.training import TreinoCreate, TreinoUpdate, TreinoOut, ExercicioCreate, ExercicioOut, ComPesoOut, SemPesoOut

def _create_exercise_details_in_db(db: Session, exercise_obj: Exercicio, exercicio_schema: ExercicioCreate):
    if exercicio_schema.tipo_exercicio == "ComPeso" and exercicio_schema.com_peso_details:
        com_peso = ComPeso(exercicio_id=exercise_obj.id, **exercicio_schema.com_peso_details.model_dump())
        db.add(com_peso)
        db.flush()
    elif exercicio_schema.tipo_exercicio == "SemPeso" and exercicio_schema.sem_peso_details:
        sem_peso = SemPeso(exercicio_id=exercise_obj.id, **exercicio_schema.sem_peso_details.model_dump())
        db.add(sem_peso)
        db.flush()

def _convert_exercicio_model_to_out_schema(exercicio_model: Exercicio) -> ExercicioOut:
    com_peso_out = None
    if exercicio_model.com_peso_details:
        com_peso_out = ComPesoOut.model_validate(exercicio_model.com_peso_details)

    sem_peso_out = None
    if exercicio_model.sem_peso_details:
        sem_peso_out = SemPesoOut.model_validate(exercicio_model.sem_peso_details)

    return ExercicioOut(
        id=exercicio_model.id,
        nome=exercicio_model.nome,
        serie=exercicio_model.serie,
        repeticoes=exercicio_model.repeticoes,
        comentario=exercicio_model.comentario,
        tipo_exercicio=exercicio_model.tipo_exercicio,
        com_peso_details=com_peso_out,
        sem_peso_details=sem_peso_out,
    )

def create_training(db: Session, treino_data: TreinoCreate, current_user_id: int) -> TreinoOut:
    db_treino = Treino(
        nome=treino_data.nome,
        usuario_id=current_user_id
    )
    db.add(db_treino)
    db.flush()

    for exercicio_schema in treino_data.exercicios:
        db_exercicio = Exercicio(
            nome=exercicio_schema.nome,
            serie=exercicio_schema.serie,
            repeticoes=exercicio_schema.repeticoes,
            comentario=exercicio_schema.comentario,
            tipo_exercicio=exercicio_schema.tipo_exercicio
        )
        db.add(db_exercicio)
        db.flush()

        _create_exercise_details_in_db(db, db_exercicio, exercicio_schema)

        treino_exercicio_link = TreinoExercicioLink(
            treino_id=db_treino.id,
            exercicio_id=db_exercicio.id
        )
        db.add(treino_exercicio_link)

    db.commit()
    db.refresh(db_treino)

    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == db_treino.usuario_id).first()
    if not user:
        raise ValueError("Usuário associado ao treino não encontrado.")

    exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in db_treino.exercicios]

    return TreinoOut(
        id=db_treino.id,
        nome=db_treino.nome,
        usuario=user,
        exercicios=exercicios_out
    )

def get_trainings_for_user(db: Session, user_id: int) -> List[TreinoOut]:
    treinos = db.execute(
        select(Treino)
        .where(Treino.usuario_id == user_id)
        .options(
            selectinload(Treino.exercicios).options(
                selectinload(Exercicio.com_peso_details),
                selectinload(Exercicio.sem_peso_details)
            )
        )
        .options(joinedload(Treino.usuario))
    ).scalars().all()

    trainings_out = []
    for treino in treinos:
        exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in treino.exercicios]
        trainings_out.append(
            TreinoOut(
                id=treino.id,
                nome=treino.nome,
                usuario=treino.usuario,
                exercicios=exercicios_out
            )
        )
    return trainings_out

def get_training_by_id_for_user(db: Session, training_id: int, user_id: int) -> Optional[TreinoOut]:
    treino = db.execute(
        select(Treino)
        .where(Treino.id == training_id, Treino.usuario_id == user_id)
        .options(
            selectinload(Treino.exercicios).options(
                selectinload(Exercicio.com_peso_details),
                selectinload(Exercicio.sem_peso_details)
            )
        )
        .options(joinedload(Treino.usuario))
    ).scalars().first()

    if not treino:
        return None
    
    exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in treino.exercicios]
    return TreinoOut(
        id=treino.id,
        nome=treino.nome,
        usuario=treino.usuario,
        exercicios=exercicios_out
    )

def update_training(db: Session, training_id: int, user_id: int, treino_data: TreinoUpdate) -> Optional[TreinoOut]:
    treino = db.execute(
        select(Treino)
        .where(Treino.id == training_id, Treino.usuario_id == user_id)
    ).scalars().first()

    if not treino:
        return None

    treino.nome = treino_data.nome if treino_data.nome is not None else treino.nome
    
    db.add(treino)
    db.commit()
    db.refresh(treino)

    updated_treino = db.execute(
        select(Treino)
        .where(Treino.id == treino.id)
        .options(
            selectinload(Treino.exercicios).options(
                selectinload(Exercicio.com_peso_details),
                selectinload(Exercicio.sem_peso_details)
            )
        )
        .options(joinedload(Treino.usuario))
    ).scalars().first()

    exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in updated_treino.exercicios]

    return TreinoOut(
        id=updated_treino.id,
        nome=updated_treino.nome,
        usuario=updated_treino.usuario,
        exercicios=exercicios_out
    )

def delete_training(db: Session, training_id: int, user_id: int) -> bool:
    treino = db.execute(
        select(Treino)
        .where(Treino.id == training_id, Treino.usuario_id == user_id)
    ).scalars().first()

    if not treino:
        return False

    db.delete(treino)
    db.commit()
    return True

