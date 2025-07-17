import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from datetime import datetime
from app.services import exercise_service
from app.models.exercise import Exercicio, ComPeso, SemPeso
from app.schemas.exercise import (
    ExercicioCreate,
    ExercicioUpdate,
    ComPesoCreate,
    SemPesoCreate,
)
from app.models.training import Treino


class TestExerciseService:
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)

    @pytest.fixture
    def mock_exercicio_com_peso(self):
        exercicio = Mock(spec=Exercicio)
        exercicio.id = 1
        exercicio.nome = "Supino"
        exercicio.serie = 4
        exercicio.repeticoes = 8
        exercicio.comentario = "Teste"
        exercicio.tipo_exercicio = "COM_PESO"
        exercicio.grupo_muscular = "PEITO"
        exercicio.dificuldade = "INTERMEDIARIO"
        exercicio.instrucoes = "Deite no banco e empurre a barra"
        exercicio.tempo_descanso_seg = 90
        exercicio.is_composto = True
        exercicio.equipamento = "Barra"
        exercicio.created_at = datetime.now()
        exercicio.updated_at = datetime.now()

        com_peso = Mock(spec=ComPeso)
        com_peso.id = 1
        com_peso.exercicio_id = 1
        com_peso.peso_kg = 80.0
        com_peso.peso_maximo_kg = 100.0
        com_peso.incremento_sugerido_kg = 2.5

        exercicio.com_peso_details = com_peso
        exercicio.sem_peso_details = None

        return exercicio

    @pytest.fixture
    def mock_exercicio_sem_peso(self):
        exercicio = Mock(spec=Exercicio)
        exercicio.id = 2
        exercicio.nome = "Corrida"
        exercicio.serie = 1
        exercicio.repeticoes = 1
        exercicio.comentario = "Cardio"
        exercicio.tipo_exercicio = "SEM_PESO"
        exercicio.grupo_muscular = "CARDIO"
        exercicio.dificuldade = "INICIANTE"
        exercicio.instrucoes = "Corra em ritmo constante"
        exercicio.tempo_descanso_seg = 60
        exercicio.is_composto = False
        exercicio.equipamento = None
        exercicio.created_at = datetime.now()
        exercicio.updated_at = datetime.now()

        sem_peso = Mock(spec=SemPeso)
        sem_peso.id = 1
        sem_peso.exercicio_id = 2
        sem_peso.tempo_seg = 1800.0
        sem_peso.distancia_m = 5000.0
        sem_peso.meta_velocidade = 2.78
        sem_peso.calorias_estimadas = 300.0
        sem_peso.intensidade = "moderada"

        exercicio.com_peso_details = None
        exercicio.sem_peso_details = sem_peso

        return exercicio

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service._create_exercise_details_in_db")
    @patch("app.services.exercise_service.Exercicio")
    @patch("app.services.exercise_service.ComPeso")
    def test_create_exercise_com_peso_success(
        self,
        mock_com_peso,
        mock_exercicio_class,
        mock_create_details,
        mock_convert,
        mock_db,
        mock_exercicio_com_peso,
    ):
        exercicio_data = ExercicioCreate(
            nome="Supino",
            serie=4,
            repeticoes=8,
            comentario="Teste",
            tipo_exercicio="COM_PESO",
            grupo_muscular="PEITO",
            dificuldade="INTERMEDIARIO",
            instrucoes="Deite no banco e empurre a barra",
            tempo_descanso_seg=90,
            com_peso_details=ComPesoCreate(peso_kg=80.0),
        )

        mock_exercicio_class.return_value = mock_exercicio_com_peso
        mock_convert.return_value = Mock()

        mock_db.add = Mock()
        mock_db.flush = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        result = exercise_service.create_exercise(mock_db, exercicio_data)

        assert mock_db.add.called
        assert mock_db.flush.called
        assert mock_db.commit.called
        assert mock_create_details.called

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service._create_exercise_details_in_db")
    @patch("app.services.exercise_service.Exercicio")
    @patch("app.services.exercise_service.SemPeso")
    def test_create_exercise_sem_peso_success(
        self,
        mock_sem_peso,
        mock_exercicio_class,
        mock_create_details,
        mock_convert,
        mock_db,
        mock_exercicio_sem_peso,
    ):
        exercicio_data = ExercicioCreate(
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
                tempo_seg=1800.0, distancia_m=5000.0, meta_velocidade=2.78
            ),
        )

        mock_exercicio_class.return_value = mock_exercicio_sem_peso
        mock_convert.return_value = Mock()

        mock_db.add = Mock()
        mock_db.flush = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        result = exercise_service.create_exercise(mock_db, exercicio_data)

        assert mock_db.add.called
        assert mock_db.flush.called
        assert mock_db.commit.called
        assert mock_create_details.called

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_get_exercise_by_id_found(
        self,
        mock_select,
        mock_selectinload,
        mock_convert,
        mock_db,
        mock_exercicio_com_peso,
    ):
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_exercicio_com_peso
        mock_db.execute.return_value = mock_result

        mock_convert.return_value = Mock()

        result = exercise_service.get_exercise_by_id(mock_db, 1)

        assert result is not None
        assert mock_db.execute.called

    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_get_exercise_by_id_not_found(
        self, mock_select, mock_selectinload, mock_db
    ):
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        result = exercise_service.get_exercise_by_id(mock_db, 999)

        assert result is None

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_get_exercises_by_type_com_peso(
        self,
        mock_select,
        mock_selectinload,
        mock_convert,
        mock_db,
        mock_exercicio_com_peso,
    ):
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_exercicio_com_peso]
        mock_db.execute.return_value = mock_result

        mock_convert.return_value = Mock()

        result = exercise_service.get_exercises_by_type(mock_db, "COM_PESO")

        assert len(result) == 1
        assert mock_db.execute.called

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_get_exercises_by_type_sem_peso(
        self,
        mock_select,
        mock_selectinload,
        mock_convert,
        mock_db,
        mock_exercicio_sem_peso,
    ):
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_exercicio_sem_peso]
        mock_db.execute.return_value = mock_result

        mock_convert.return_value = Mock()

        result = exercise_service.get_exercises_by_type(mock_db, "SEM_PESO")

        assert len(result) == 1
        assert mock_db.execute.called

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_get_all_exercises(
        self,
        mock_select,
        mock_selectinload,
        mock_convert,
        mock_db,
        mock_exercicio_com_peso,
        mock_exercicio_sem_peso,
    ):
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [
            mock_exercicio_com_peso,
            mock_exercicio_sem_peso,
        ]
        mock_db.execute.return_value = mock_result

        mock_convert.return_value = Mock()

        result = exercise_service.get_all_exercises(mock_db)

        assert len(result) == 2
        assert mock_db.execute.called

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_update_exercise_com_peso_success(
        self,
        mock_select,
        mock_selectinload,
        mock_convert,
        mock_db,
        mock_exercicio_com_peso,
    ):
        update_data = ExercicioUpdate(
            nome="Supino Atualizado", serie=5, com_peso_details={"peso_kg": 90.0}
        )

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_exercicio_com_peso
        mock_db.execute.return_value = mock_result
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        mock_convert.return_value = Mock()

        result = exercise_service.update_exercise(mock_db, 1, update_data)

        assert result is not None
        assert mock_db.commit.called

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_update_exercise_sem_peso_success(
        self,
        mock_select,
        mock_selectinload,
        mock_convert,
        mock_db,
        mock_exercicio_sem_peso,
    ):
        update_data = ExercicioUpdate(
            nome="Corrida Atualizada",
            sem_peso_details={"tempo_seg": 2400.0, "distancia_m": 6000.0},
        )

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_exercicio_sem_peso
        mock_db.execute.return_value = mock_result
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        mock_convert.return_value = Mock()

        result = exercise_service.update_exercise(mock_db, 2, update_data)

        assert result is not None
        assert mock_db.commit.called

    @patch("app.services.exercise_service.select")
    def test_update_exercise_not_found(self, mock_select, mock_db):
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        update_data = ExercicioUpdate(nome="Nome Atualizado")

        result = exercise_service.update_exercise(mock_db, 999, update_data)

        assert result is None

    @patch("app.services.exercise_service.select")
    def test_delete_exercise_success(
        self, mock_select, mock_db, mock_exercicio_com_peso
    ):
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_exercicio_com_peso
        mock_db.execute.return_value = mock_result
        mock_db.delete = Mock()
        mock_db.commit = Mock()

        result = exercise_service.delete_exercise(mock_db, 1)

        assert result is True
        mock_db.delete.assert_called_with(mock_exercicio_com_peso)
        assert mock_db.commit.called

    @patch("app.services.exercise_service.select")
    def test_delete_exercise_not_found(self, mock_select, mock_db):
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        result = exercise_service.delete_exercise(mock_db, 999)

        assert result is False
        mock_db.delete.assert_not_called()

    @patch("app.services.exercise_service.select")
    def test_delete_exercise_with_training_links(
        self, mock_select, mock_db, mock_exercicio_com_peso
    ):
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_exercicio_com_peso
        mock_db.execute.return_value = mock_result
        mock_db.delete = Mock()
        mock_db.commit = Mock()

        mock_links_result = Mock()
        mock_links_result.scalars.return_value.all.return_value = [Mock()]
        mock_db.execute.side_effect = [mock_result, mock_links_result]

        result = exercise_service.delete_exercise(mock_db, 1)

        assert result is True
        assert mock_db.delete.call_count >= 2
        assert mock_db.commit.called

    @patch("app.services.exercise_service._convert_exercicio_model_to_out_schema")
    @patch("app.services.exercise_service.selectinload")
    @patch("app.services.exercise_service.select")
    def test_get_exercises_in_training(
        self,
        mock_select,
        mock_selectinload,
        mock_convert,
        mock_db,
        mock_exercicio_com_peso,
    ):
        # Criar mock do treino com exercicios
        mock_treino = Mock()
        mock_treino.exercicios = [mock_exercicio_com_peso]

        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_treino
        mock_db.execute.return_value = mock_result

        mock_convert.return_value = Mock()

        result = exercise_service.get_exercises_in_training(mock_db, 1)

        assert len(result) == 1
        assert mock_db.execute.called

    def test_convert_exercicio_model_to_out_schema_com_peso(
        self, mock_exercicio_com_peso
    ):
        result = exercise_service._convert_exercicio_model_to_out_schema(
            mock_exercicio_com_peso
        )

        assert result.nome == "Supino"
        assert result.tipo_exercicio == "COM_PESO"
        assert result.com_peso_details is not None
        assert result.sem_peso_details is None

    def test_convert_exercicio_model_to_out_schema_sem_peso(
        self, mock_exercicio_sem_peso
    ):
        result = exercise_service._convert_exercicio_model_to_out_schema(
            mock_exercicio_sem_peso
        )

        assert result.nome == "Corrida"
        assert result.tipo_exercicio == "SEM_PESO"
        assert result.com_peso_details is None
        assert result.sem_peso_details is not None

    def test_create_exercise_details_in_db_com_peso(self, mock_db):
        exercicio_obj = Mock()
        exercicio_obj.id = 1

        exercicio_schema = ExercicioCreate(
            nome="Supino",
            serie=4,
            repeticoes=8,
            comentario="Teste",
            tipo_exercicio="COM_PESO",
            grupo_muscular="PEITO",
            dificuldade="INTERMEDIARIO",
            instrucoes="Deite no banco e empurre a barra",
            tempo_descanso_seg=90,
            com_peso_details=ComPesoCreate(peso_kg=80.0),
        )

        mock_db.add = Mock()
        mock_db.flush = Mock()

        exercise_service._create_exercise_details_in_db(
            mock_db, exercicio_obj, exercicio_schema
        )

        assert mock_db.add.called
        assert mock_db.flush.called

    def test_create_exercise_details_in_db_sem_peso(self, mock_db):
        exercicio_obj = Mock()
        exercicio_obj.id = 1

        exercicio_schema = ExercicioCreate(
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
                tempo_seg=1800.0, distancia_m=5000.0, meta_velocidade=2.78
            ),
        )

        mock_db.add = Mock()
        mock_db.flush = Mock()

        exercise_service._create_exercise_details_in_db(
            mock_db, exercicio_obj, exercicio_schema
        )

        assert mock_db.add.called
        assert mock_db.flush.called
