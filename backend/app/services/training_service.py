from typing import List, Optional
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

from app.models.training import Treino
from app.models.exercise import Exercicio, ComPeso, SemPeso, TipoExercicio
from app.models.user import User as SQLAlchemyUser
from app.schemas.training import TreinoCreate, TreinoUpdate, TreinoOut
from app.schemas.exercise import ExercicioCreate, ExercicioOut, ComPesoOut, SemPesoOut

def _create_exercise_details_in_db(db: Session, exercise_obj: Exercicio, exercicio_schema: ExercicioCreate):
    if exercicio_schema.tipo_exercicio == TipoExercicio.COM_PESO and exercicio_schema.com_peso_details:
        com_peso = ComPeso(exercicio_id=exercise_obj.id, **exercicio_schema.com_peso_details.model_dump())
        db.add(com_peso)
        db.flush()
    elif exercicio_schema.tipo_exercicio == TipoExercicio.SEM_PESO and exercicio_schema.sem_peso_details:
        sem_peso = SemPeso(exercicio_id=exercise_obj.id, **exercicio_schema.sem_peso_details.model_dump())
        db.add(sem_peso)
        db.flush()

def _convert_exercicio_model_to_out_schema(exercicio_model: Exercicio) -> ExercicioOut:
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

def create_training(db: Session, treino_data: TreinoCreate, current_user_id: int) -> TreinoOut:
    db_treino = Treino(
        nome=treino_data.nome,
        usuario_id=current_user_id
    )
    db.add(db_treino)
    db.flush()

    for exercicio_data in treino_data.exercicios:
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
            tipo_exercicio=exercicio_data.tipo_exercicio
        )
        db.add(db_exercicio)
        db.flush()

        _create_exercise_details_in_db(db, db_exercicio, exercicio_data)

        db_treino.exercicios.append(db_exercicio)

    db.commit()
    db.refresh(db_treino)

    exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in db_treino.exercicios]
    
    return TreinoOut(
        id=db_treino.id,
        nome=db_treino.nome,
        descricao=db_treino.descricao,
        categoria=db_treino.categoria,
        duracao_estimada_min=db_treino.duracao_estimada_min,
        usuario_id=db_treino.usuario_id,
        status=db_treino.status,
        duracao_real_min=db_treino.duracao_real_min,
        calorias_queimadas=db_treino.calorias_queimadas,
        volume_total_kg=db_treino.volume_total_kg,
        dificuldade_percebida=db_treino.dificuldade_percebida,
        satisfacao=db_treino.satisfacao,
        observacoes=db_treino.observacoes,
        created_at=db_treino.created_at,
        updated_at=db_treino.updated_at,
        iniciado_em=db_treino.iniciado_em,
        finalizado_em=db_treino.finalizado_em,
        exercicios=exercicios_out
    )

def get_trainings_for_user(db: Session, user_id: int) -> List[TreinoOut]:
    treinos = db.execute(
        select(Treino)
        .where(Treino.usuario_id == user_id)
        .options(
            selectinload(Treino.exercicios).selectinload(Exercicio.com_peso_details),
            selectinload(Treino.exercicios).selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().all()

    result = []
    for treino in treinos:
        exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in treino.exercicios]
        result.append(TreinoOut(
            id=treino.id,
            nome=treino.nome,
            descricao=treino.descricao,
            categoria=treino.categoria,
            duracao_estimada_min=treino.duracao_estimada_min,
            usuario_id=treino.usuario_id,
            status=treino.status,
            duracao_real_min=treino.duracao_real_min,
            calorias_queimadas=treino.calorias_queimadas,
            volume_total_kg=treino.volume_total_kg,
            dificuldade_percebida=treino.dificuldade_percebida,
            satisfacao=treino.satisfacao,
            observacoes=treino.observacoes,
            created_at=treino.created_at,
            updated_at=treino.updated_at,
            iniciado_em=treino.iniciado_em,
            finalizado_em=treino.finalizado_em,
            exercicios=exercicios_out
        ))

    return result

def get_training_by_id_for_user(db: Session, training_id: int, user_id: int) -> Optional[TreinoOut]:
    treino = db.execute(
        select(Treino)
        .where(Treino.id == training_id, Treino.usuario_id == user_id)
        .options(
            selectinload(Treino.exercicios).selectinload(Exercicio.com_peso_details),
            selectinload(Treino.exercicios).selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().first()

    if not treino:
        return None

    exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in treino.exercicios]
    
    return TreinoOut(
        id=treino.id,
        nome=treino.nome,
        descricao=treino.descricao,
        categoria=treino.categoria,
        duracao_estimada_min=treino.duracao_estimada_min,
        usuario_id=treino.usuario_id,
        status=treino.status,
        duracao_real_min=treino.duracao_real_min,
        calorias_queimadas=treino.calorias_queimadas,
        volume_total_kg=treino.volume_total_kg,
        dificuldade_percebida=treino.dificuldade_percebida,
        satisfacao=treino.satisfacao,
        observacoes=treino.observacoes,
        created_at=treino.created_at,
        updated_at=treino.updated_at,
        iniciado_em=treino.iniciado_em,
        finalizado_em=treino.finalizado_em,
        exercicios=exercicios_out
    )

def update_training(db: Session, training_id: int, user_id: int, treino_data: TreinoUpdate) -> Optional[TreinoOut]:
    treino = db.execute(
        select(Treino)
        .where(Treino.id == training_id, Treino.usuario_id == user_id)
        .options(
            selectinload(Treino.exercicios).selectinload(Exercicio.com_peso_details),
            selectinload(Treino.exercicios).selectinload(Exercicio.sem_peso_details)
        )
    ).scalars().first()

    if not treino:
        return None

    if treino_data.nome is not None:
        treino.nome = treino_data.nome

    db.add(treino)
    db.commit()
    db.refresh(treino)

    exercicios_out = [_convert_exercicio_model_to_out_schema(e) for e in treino.exercicios]
    
    return TreinoOut(
        id=treino.id,
        nome=treino.nome,
        descricao=treino.descricao,
        categoria=treino.categoria,
        duracao_estimada_min=treino.duracao_estimada_min,
        usuario_id=treino.usuario_id,
        status=treino.status,
        duracao_real_min=treino.duracao_real_min,
        calorias_queimadas=treino.calorias_queimadas,
        volume_total_kg=treino.volume_total_kg,
        dificuldade_percebida=treino.dificuldade_percebida,
        satisfacao=treino.satisfacao,
        observacoes=treino.observacoes,
        created_at=treino.created_at,
        updated_at=treino.updated_at,
        iniciado_em=treino.iniciado_em,
        finalizado_em=treino.finalizado_em,
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

