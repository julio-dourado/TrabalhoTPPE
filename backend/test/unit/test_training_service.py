import pytest
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session
from app.services import training_service
from app.models.training import Treino
from app.models.exercise import Exercicio, ComPeso, SemPeso
from app.models.user import User
from app.schemas.training import TreinoCreate, TreinoUpdate
from app.schemas.exercise import ExercicioCreate, ComPesoCreate, SemPesoCreate
from datetime import datetime

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def sample_user():
    user = Mock(spec=User)
    user.id = 1
    user.nome = "Usuário Teste"
    user.email = "teste@exemplo.com"
    return user

@pytest.fixture
def sample_treino_create():
    return TreinoCreate(
        nome="Treino Teste",
        exercicios=[
            ExercicioCreate(
                nome="Supino",
                serie=3,
                repeticoes=10,
                comentario="Teste",
                tipo_exercicio="COM_PESO",
                grupo_muscular="PEITO",
                dificuldade="INTERMEDIARIO",
                instrucoes="Deite no banco e empurre a barra",
                tempo_descanso_seg=90,
                com_peso_details=ComPesoCreate(peso_kg=50.0)
            )
        ]
    )

@pytest.fixture
def sample_treino_cardio_create():
    return TreinoCreate(
        nome="Treino Cardio",
        exercicios=[
            ExercicioCreate(
                nome="Corrida",
                serie=1,
                repeticoes=1,
                comentario="Cardio",
                tipo_exercicio="SEM_PESO",
                grupo_muscular="CARDIO",
                dificuldade="INICIANTE",
                instrucoes="Corra em ritmo constante",
                tempo_descanso_seg=60,
                sem_peso_details=SemPesoCreate(
                    tempo_seg=1800.0,
                    distancia_m=5000.0,
                    meta_velocidade=2.8
                )
            )
        ]
    )

@patch('app.services.training_service._convert_exercicio_model_to_out_schema')
@patch('app.services.training_service.Treino')
@patch('app.services.training_service.Exercicio')
@patch('app.services.training_service.ComPeso')
def test_create_training_with_weight_exercise(mock_com_peso, mock_exercicio_class, mock_treino_class, mock_convert, mock_db, sample_user, sample_treino_create):
    mock_treino_instance = Mock()
    mock_treino_instance.id = 1
    mock_treino_instance.nome = "Treino Teste"
    mock_treino_instance.usuario_id = 1
    mock_treino_instance.usuario = sample_user
    mock_treino_instance.exercicios = []
    mock_treino_instance.descricao = "Treino de teste"
    mock_treino_instance.categoria = "FORCA"
    mock_treino_instance.duracao_estimada_min = 60
    mock_treino_instance.status = "PLANEJADO"
    mock_treino_instance.duracao_real_min = None
    mock_treino_instance.calorias_queimadas = None
    mock_treino_instance.volume_total_kg = None
    mock_treino_instance.dificuldade_percebida = None
    mock_treino_instance.satisfacao = None
    mock_treino_instance.observacoes = None
    mock_treino_instance.created_at = datetime.now()
    mock_treino_instance.updated_at = datetime.now()
    mock_treino_instance.iniciado_em = None
    mock_treino_instance.finalizado_em = None
    
    mock_exercicio_instance = Mock()
    mock_exercicio_instance.id = 1
    mock_exercicio_instance.nome = "Supino"
    
    from app.schemas.exercise import ExercicioOut, ComPesoOut
    mock_exercicio_out = ExercicioOut(
        id=1,
        nome="Supino",
        serie=3,
        repeticoes=10,
        comentario="Teste",
        tipo_exercicio="COM_PESO",
        grupo_muscular="PEITO",
        dificuldade="INTERMEDIARIO",
        instrucoes="Deite no banco e empurre a barra",
        tempo_descanso_seg=90,
        is_composto=False,
        equipamento=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        com_peso_details=ComPesoOut(
            id=1, 
            exercicio_id=1, 
            peso_kg=50.0, 
            peso_maximo_kg=100.0, 
            incremento_sugerido_kg=2.5
        ),
        sem_peso_details=None
    )
    mock_convert.return_value = mock_exercicio_out
    
    mock_treino_class.return_value = mock_treino_instance
    mock_exercicio_class.return_value = mock_exercicio_instance
    
    mock_db.add = Mock()
    mock_db.flush = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    result = training_service.create_training(mock_db, sample_treino_create, sample_user.id)
    
    assert mock_db.add.call_count >= 2
    assert mock_db.commit.called
    assert result.nome == "Treino Teste"
    assert result.id == 1

@patch('app.services.training_service._convert_exercicio_model_to_out_schema')
@patch('app.services.training_service.Treino')
@patch('app.services.training_service.Exercicio')
@patch('app.services.training_service.SemPeso')
def test_create_training_with_cardio_exercise(mock_sem_peso, mock_exercicio_class, mock_treino_class, mock_convert, mock_db, sample_user, sample_treino_cardio_create):
    mock_treino_instance = Mock()
    mock_treino_instance.id = 1
    mock_treino_instance.nome = "Treino Cardio"
    mock_treino_instance.usuario_id = 1
    mock_treino_instance.usuario = sample_user
    mock_treino_instance.exercicios = []
    mock_treino_instance.descricao = "Treino de cardio"
    mock_treino_instance.categoria = "CARDIO"
    mock_treino_instance.duracao_estimada_min = 30
    mock_treino_instance.status = "PLANEJADO"
    mock_treino_instance.duracao_real_min = None
    mock_treino_instance.calorias_queimadas = None
    mock_treino_instance.volume_total_kg = None
    mock_treino_instance.dificuldade_percebida = None
    mock_treino_instance.satisfacao = None
    mock_treino_instance.observacoes = None
    mock_treino_instance.created_at = datetime.now()
    mock_treino_instance.updated_at = datetime.now()
    mock_treino_instance.iniciado_em = None
    mock_treino_instance.finalizado_em = None
    
    mock_exercicio_instance = Mock()
    mock_exercicio_instance.id = 1
    mock_exercicio_instance.nome = "Corrida"
    
    from app.schemas.exercise import ExercicioOut, SemPesoOut
    mock_exercicio_out = ExercicioOut(
        id=1,
        nome="Corrida",
        serie=1,
        repeticoes=1,
        comentario="Cardio",
        tipo_exercicio="SEM_PESO",
        grupo_muscular="CARDIO",
        dificuldade="INICIANTE",
        instrucoes="Corra em ritmo constante",
        tempo_descanso_seg=60,
        is_composto=False,
        equipamento=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        com_peso_details=None,
        sem_peso_details=SemPesoOut(
            id=1, 
            exercicio_id=1, 
            tempo_seg=1800.0, 
            distancia_m=5000.0, 
            meta_velocidade=2.8,
            calorias_estimadas=300.0,
            intensidade="moderada"
        )
    )
    mock_convert.return_value = mock_exercicio_out
    
    mock_treino_class.return_value = mock_treino_instance
    mock_exercicio_class.return_value = mock_exercicio_instance
    
    mock_db.add = Mock()
    mock_db.flush = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    result = training_service.create_training(mock_db, sample_treino_cardio_create, sample_user.id)
    
    assert mock_db.add.call_count >= 2
    assert mock_db.commit.called
    assert result.nome == "Treino Cardio"
    assert result.id == 1

def test_get_trainings_for_user(mock_db, sample_user):
    mock_treino = Mock()
    mock_treino.id = 1
    mock_treino.nome = "Treino Teste"
    mock_treino.usuario = sample_user
    mock_treino.exercicios = []
    mock_treino.descricao = "Treino de teste"
    mock_treino.categoria = "FORCA"
    mock_treino.duracao_estimada_min = 60
    mock_treino.usuario_id = sample_user.id
    mock_treino.status = "PLANEJADO"
    mock_treino.duracao_real_min = None
    mock_treino.calorias_queimadas = None
    mock_treino.volume_total_kg = None
    mock_treino.dificuldade_percebida = None
    mock_treino.satisfacao = None
    mock_treino.observacoes = None
    mock_treino.created_at = datetime.now()
    mock_treino.updated_at = datetime.now()
    mock_treino.iniciado_em = None
    mock_treino.finalizado_em = None
    
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = [mock_treino]
    
    mock_db.execute.return_value = mock_result
    
    result = training_service.get_trainings_for_user(mock_db, sample_user.id)
    
    assert len(result) == 1
    assert result[0].nome == "Treino Teste"
    assert mock_db.execute.called

def test_get_training_by_id_for_user_found(mock_db, sample_user):
    mock_treino = Mock()
    mock_treino.id = 1
    mock_treino.nome = "Treino Encontrado"
    mock_treino.usuario = sample_user
    mock_treino.exercicios = []
    mock_treino.descricao = "Treino encontrado"
    mock_treino.categoria = "FORCA"
    mock_treino.duracao_estimada_min = 60
    mock_treino.usuario_id = sample_user.id
    mock_treino.status = "PLANEJADO"
    mock_treino.duracao_real_min = None
    mock_treino.calorias_queimadas = None
    mock_treino.volume_total_kg = None
    mock_treino.dificuldade_percebida = None
    mock_treino.satisfacao = None
    mock_treino.observacoes = None
    mock_treino.created_at = datetime.now()
    mock_treino.updated_at = datetime.now()
    mock_treino.iniciado_em = None
    mock_treino.finalizado_em = None
    
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = mock_treino
    
    mock_db.execute.return_value = mock_result
    
    result = training_service.get_training_by_id_for_user(mock_db, 1, sample_user.id)
    
    assert result is not None
    assert result.nome == "Treino Encontrado"

def test_get_training_by_id_for_user_not_found(mock_db, sample_user):
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = None
    
    mock_db.execute.return_value = mock_result
    
    result = training_service.get_training_by_id_for_user(mock_db, 999, sample_user.id)
    
    assert result is None

def test_update_training_success(mock_db, sample_user):
    mock_treino = Mock()
    mock_treino.id = 1
    mock_treino.nome = "Nome Original"
    mock_treino.usuario_id = sample_user.id
    mock_treino.usuario = sample_user
    mock_treino.exercicios = []
    mock_treino.descricao = "Treino original"
    mock_treino.categoria = "FORCA"
    mock_treino.duracao_estimada_min = 60
    mock_treino.status = "PLANEJADO"
    mock_treino.duracao_real_min = None
    mock_treino.calorias_queimadas = None
    mock_treino.volume_total_kg = None
    mock_treino.dificuldade_percebida = None
    mock_treino.satisfacao = None
    mock_treino.observacoes = None
    mock_treino.created_at = datetime.now()
    mock_treino.updated_at = datetime.now()
    mock_treino.iniciado_em = None
    mock_treino.finalizado_em = None
    
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = mock_treino
    
    mock_db.execute.return_value = mock_result
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    update_data = TreinoUpdate(nome="Nome Atualizado")
    result = training_service.update_training(mock_db, 1, sample_user.id, update_data)
    
    assert result is not None
    assert mock_treino.nome == "Nome Atualizado"
    assert mock_db.commit.called

def test_update_training_not_found(mock_db, sample_user):
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = None
    
    mock_db.execute.return_value = mock_result
    
    update_data = TreinoUpdate(nome="Nome Atualizado")
    result = training_service.update_training(mock_db, 999, sample_user.id, update_data)
    
    assert result is None

def test_delete_training_success(mock_db, sample_user):
    mock_treino = Mock()
    mock_treino.id = 1
    mock_treino.usuario_id = sample_user.id
    
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = mock_treino
    
    mock_db.execute.return_value = mock_result
    mock_db.delete = Mock()
    mock_db.commit = Mock()
    
    result = training_service.delete_training(mock_db, 1, sample_user.id)
    
    assert result is True
    assert mock_db.delete.called
    assert mock_db.commit.called

def test_delete_training_not_found(mock_db, sample_user):
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = None
    
    mock_db.execute.return_value = mock_result
    
    result = training_service.delete_training(mock_db, 999, sample_user.id)
    
    assert result is False

def test_convert_exercicio_model_to_out_schema_with_peso():
    mock_exercicio = Mock()
    mock_exercicio.id = 1
    mock_exercicio.nome = "Supino"
    mock_exercicio.serie = 3
    mock_exercicio.repeticoes = 10
    mock_exercicio.comentario = "Teste"
    mock_exercicio.tipo_exercicio = "COM_PESO"
    mock_exercicio.grupo_muscular = "PEITO"
    mock_exercicio.dificuldade = "INTERMEDIARIO"
    mock_exercicio.instrucoes = "Deite no banco e empurre a barra"
    mock_exercicio.tempo_descanso_seg = 90
    mock_exercicio.is_composto = True
    mock_exercicio.equipamento = "Barra"
    mock_exercicio.created_at = datetime.now()
    mock_exercicio.updated_at = datetime.now()
    
    mock_com_peso = Mock()
    mock_com_peso.id = 1
    mock_com_peso.exercicio_id = 1
    mock_com_peso.peso_kg = 50.0
    mock_com_peso.peso_maximo_kg = 100.0
    mock_com_peso.incremento_sugerido_kg = 2.5
    
    mock_exercicio.com_peso_details = mock_com_peso
    mock_exercicio.sem_peso_details = None
    
    result = training_service._convert_exercicio_model_to_out_schema(mock_exercicio)
    
    assert result.nome == "Supino"
    assert result.tipo_exercicio == "COM_PESO"
    assert result.com_peso_details is not None
    assert result.com_peso_details.peso_kg == 50.0

def test_convert_exercicio_model_to_out_schema_sem_peso():
    mock_exercicio = Mock()
    mock_exercicio.id = 2
    mock_exercicio.nome = "Corrida"
    mock_exercicio.serie = 1
    mock_exercicio.repeticoes = 1
    mock_exercicio.comentario = "Cardio"
    mock_exercicio.tipo_exercicio = "SEM_PESO"
    mock_exercicio.grupo_muscular = "CARDIO"
    mock_exercicio.dificuldade = "INICIANTE"
    mock_exercicio.instrucoes = "Corra em ritmo constante"
    mock_exercicio.tempo_descanso_seg = 60
    mock_exercicio.is_composto = False
    mock_exercicio.equipamento = None
    mock_exercicio.created_at = datetime.now()
    mock_exercicio.updated_at = datetime.now()
    
    mock_sem_peso = Mock()
    mock_sem_peso.id = 1
    mock_sem_peso.exercicio_id = 2
    mock_sem_peso.tempo_seg = 1800.0
    mock_sem_peso.distancia_m = 5000.0
    mock_sem_peso.meta_velocidade = 2.8
    mock_sem_peso.calorias_estimadas = 300.0
    mock_sem_peso.intensidade = "moderada"
    
    mock_exercicio.com_peso_details = None
    mock_exercicio.sem_peso_details = mock_sem_peso
    
    result = training_service._convert_exercicio_model_to_out_schema(mock_exercicio)
    
    assert result.nome == "Corrida"
    assert result.tipo_exercicio == "SEM_PESO"
    assert result.sem_peso_details is not None
    assert result.sem_peso_details.tempo_seg == 1800.0 