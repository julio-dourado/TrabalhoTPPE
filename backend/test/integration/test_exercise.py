import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User as SQLAlchemyUser
from app.models.exercise import Exercicio, ComPeso, SemPeso, GrupoMuscular, Dificuldade, TipoExercicio
from app.models.training import Treino
from app.services import exercise_service

# Note: As fixtures 'client_with_db' e 'db_session' são importadas
# automaticamente de conftest.py pelo pytest.

class TestExerciseRoutes:
    """Testes das rotas de exercícios"""

    def test_create_exercise_com_peso_success(self, client_with_db: TestClient):
        """
        US11: Teste de criação de exercício com peso
        """
        exercise_data = {
            "nome": "Supino",
            "grupo_muscular": "PEITO",
            "dificuldade": "INICIANTE",
            "serie": 4,
            "repeticoes": 8,
            "comentario": "Foco no peito",
            "instrucoes": "Deite no banco, pegue a barra com pegada média",
            "tempo_descanso_seg": 90,
            "is_composto": True,
            "equipamento": "Barra olímpica",
            "tipo_exercicio": "COM_PESO",
            "com_peso_details": {
                "peso_kg": 80.0,
                "peso_maximo_kg": 100.0,
                "incremento_sugerido_kg": 2.5
            }
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Supino"
        assert data["grupo_muscular"] == "PEITO"
        assert data["serie"] == 4
        assert data["repeticoes"] == 8
        assert data["tipo_exercicio"] == "COM_PESO"
        assert data["com_peso_details"]["peso_kg"] == 80.0
        assert data["sem_peso_details"] is None
        assert "id" in data

    def test_create_exercise_sem_peso_success(self, client_with_db: TestClient):
        """
        US14: Teste de criação de exercício sem peso
        """
        exercise_data = {
            "nome": "Corrida",
            "grupo_muscular": "CARDIO",
            "dificuldade": "INTERMEDIARIO",
            "serie": 1,
            "repeticoes": 1,
            "comentario": "Cardio matinal",
            "instrucoes": "Mantenha ritmo constante",
            "tempo_descanso_seg": 0,
            "is_composto": False,
            "equipamento": "Esteira",
            "tipo_exercicio": "SEM_PESO",
            "sem_peso_details": {
                "tempo_seg": 1800.0,
                "distancia_m": 5000.0,
                "calorias_estimadas": 300.0,
                "intensidade": "moderada"
            }
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Corrida"
        assert data["grupo_muscular"] == "CARDIO"
        assert data["tipo_exercicio"] == "SEM_PESO"
        assert data["sem_peso_details"]["tempo_seg"] == 1800.0
        assert data["sem_peso_details"]["distancia_m"] == 5000.0
        assert data["sem_peso_details"]["calorias_estimadas"] == 300.0
        assert data["com_peso_details"] is None

    def test_create_exercise_invalid_tipo(self, client_with_db: TestClient):
        """Teste de validação de tipo de exercício inválido"""
        exercise_data = {
            "nome": "Exercício Inválido",
            "grupo_muscular": "PEITO",
            "serie": 3,
            "repeticoes": 10,
            "tipo_exercicio": "TipoInvalido"
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        assert response.status_code == 422

    def test_create_exercise_com_peso_without_details(self, client_with_db: TestClient):
        """Teste de validação: exercício com peso sem detalhes"""
        exercise_data = {
            "nome": "Supino",
            "grupo_muscular": "PEITO",
            "serie": 4,
            "repeticoes": 8,
            "tipo_exercicio": "COM_PESO"
            # Faltando com_peso_details
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        assert response.status_code == 422

    def test_create_exercise_sem_peso_without_details(self, client_with_db: TestClient):
        """Teste de validação: exercício sem peso sem detalhes"""
        exercise_data = {
            "nome": "Corrida",
            "grupo_muscular": "CARDIO",
            "serie": 1,
            "repeticoes": 1,
            "tipo_exercicio": "SEM_PESO"
            # Faltando sem_peso_details
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        assert response.status_code == 422

    def test_get_all_exercises(self, client_with_db: TestClient, db_session: Session):
        """Teste de listagem de todos os exercícios"""
        # Criar exercícios de teste
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        
        # Verificar se há exercícios de ambos os tipos
        tipos = [ex["tipo_exercicio"] for ex in data]
        assert "COM_PESO" in tipos
        assert "SEM_PESO" in tipos

    def test_get_exercises_by_type_com_peso(self, client_with_db: TestClient, db_session: Session):
        """Teste de filtragem por tipo COM_PESO"""
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/?tipo=COM_PESO")
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo_exercicio"] == "COM_PESO" for ex in data)
        assert all(ex["com_peso_details"] is not None for ex in data)

    def test_get_exercises_by_type_sem_peso(self, client_with_db: TestClient, db_session: Session):
        """Teste de filtragem por tipo SEM_PESO"""
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/?tipo=SEM_PESO")
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo_exercicio"] == "SEM_PESO" for ex in data)
        assert all(ex["sem_peso_details"] is not None for ex in data)

    def test_get_exercises_invalid_type_filter(self, client_with_db: TestClient):
        """Teste de filtro com tipo inválido"""
        response = client_with_db.get("/api/v1/exercicios/?tipo=TipoInvalido")
        
        assert response.status_code == 400
        assert "Tipo deve ser 'COM_PESO' ou 'SEM_PESO'" in response.json()["detail"]

    def test_get_exercise_by_id(self, client_with_db: TestClient, db_session: Session):
        """Teste de busca de exercício por ID"""
        exercise_id = self._create_test_exercises(db_session)[0]
        
        response = client_with_db.get(f"/api/v1/exercicios/{exercise_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == exercise_id
        assert "nome" in data
        assert "tipo_exercicio" in data

    def test_get_exercise_not_found(self, client_with_db: TestClient):
        """Teste de busca de exercício inexistente"""
        response = client_with_db.get("/api/v1/exercicios/999999")
        
        assert response.status_code == 404
        assert "Exercício não encontrado" in response.json()["detail"]

    def test_update_exercise_com_peso(self, client_with_db: TestClient, db_session: Session):
        """
        US12: Teste de atualização de exercício com peso
        """
        exercise_id = self._create_test_exercises(db_session)[0]
        
        update_data = {
            "nome": "Supino Atualizado",
            "serie": 5,
            "com_peso_details": {
                "peso_kg": 90.0
            }
        }
        
        response = client_with_db.put(f"/api/v1/exercicios/{exercise_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Supino Atualizado"
        assert data["serie"] == 5
        assert data["com_peso_details"]["peso_kg"] == 90.0

    def test_update_exercise_sem_peso(self, client_with_db: TestClient, db_session: Session):
        """
        US15: Teste de atualização de exercício sem peso
        """
        exercise_ids = self._create_test_exercises(db_session)
        sem_peso_id = exercise_ids[1]  # Segundo exercício é sem peso
        
        update_data = {
            "nome": "Corrida Atualizada",
            "sem_peso_details": {
                "tempo_seg": 2400.0,
                "distancia_m": 6000.0,
                "calorias_estimadas": 400.0,
                "intensidade": "alta"
            }
        }
        
        response = client_with_db.put(f"/api/v1/exercicios/{sem_peso_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Corrida Atualizada"
        assert data["sem_peso_details"]["tempo_seg"] == 2400.0
        assert data["sem_peso_details"]["distancia_m"] == 6000.0
        assert data["sem_peso_details"]["calorias_estimadas"] == 400.0
        assert data["sem_peso_details"]["intensidade"] == "alta"

    def test_update_exercise_not_found(self, client_with_db: TestClient):
        """Teste de atualização de exercício inexistente"""
        update_data = {"nome": "Exercício Inexistente"}
        
        response = client_with_db.put("/api/v1/exercicios/999999", json=update_data)
        
        assert response.status_code == 404
        assert "Exercício não encontrado" in response.json()["detail"]

    def test_delete_exercise_com_peso(self, client_with_db: TestClient, db_session: Session):
        """
        US13: Teste de exclusão de exercício com peso
        """
        exercise_id = self._create_test_exercises(db_session)[0]
        
        response = client_with_db.delete(f"/api/v1/exercicios/{exercise_id}")
        
        assert response.status_code == 204
        
        # Verificar se foi realmente deletado
        get_response = client_with_db.get(f"/api/v1/exercicios/{exercise_id}")
        assert get_response.status_code == 404

    def test_delete_exercise_sem_peso(self, client_with_db: TestClient, db_session: Session):
        """
        US16: Teste de exclusão de exercício sem peso
        """
        exercise_ids = self._create_test_exercises(db_session)
        sem_peso_id = exercise_ids[1]
        
        response = client_with_db.delete(f"/api/v1/exercicios/{sem_peso_id}")
        
        assert response.status_code == 204
        
        # Verificar se foi realmente deletado
        get_response = client_with_db.get(f"/api/v1/exercicios/{sem_peso_id}")
        assert get_response.status_code == 404

    def test_delete_exercise_not_found(self, client_with_db: TestClient):
        """Teste de exclusão de exercício inexistente"""
        response = client_with_db.delete("/api/v1/exercicios/999999")
        
        assert response.status_code == 404
        assert "Exercício não encontrado" in response.json()["detail"]

    def test_get_weight_exercises_route(self, client_with_db: TestClient, db_session: Session):
        """Teste da rota específica para exercícios com peso"""
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/com-peso/")
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo_exercicio"] == "COM_PESO" for ex in data)
        assert all(ex["com_peso_details"] is not None for ex in data)

    def test_get_cardio_exercises_route(self, client_with_db: TestClient, db_session: Session):
        """Teste da rota específica para exercícios sem peso (cardio)"""
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/sem-peso/")
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo_exercicio"] == "SEM_PESO" for ex in data)
        assert all(ex["sem_peso_details"] is not None for ex in data)

    def _create_test_exercises(self, db: Session) -> list[int]:
        """Cria exercícios de teste e retorna os IDs"""
        # Usar o service para criar os exercícios
        from app.schemas.exercise import ExercicioCreate, ComPesoCreate, SemPesoCreate
        
        # Exercício com peso
        exercise_1 = ExercicioCreate(
            nome="Supino Teste",
            grupo_muscular=GrupoMuscular.PEITO,
            dificuldade=Dificuldade.INICIANTE,
            serie=3,
            repeticoes=10,
            comentario="Teste com peso",
            instrucoes="Instrução de teste",
            tempo_descanso_seg=60,
            is_composto=True,
            equipamento="Barra",
            tipo_exercicio=TipoExercicio.COM_PESO,
            com_peso_details=ComPesoCreate(
                peso_kg=60.0,
                peso_maximo_kg=80.0,
                incremento_sugerido_kg=2.5
            )
        )
        
        # Exercício sem peso
        exercise_2 = ExercicioCreate(
            nome="Corrida Teste",
            grupo_muscular=GrupoMuscular.CARDIO,
            dificuldade=Dificuldade.INTERMEDIARIO,
            serie=1,
            repeticoes=1,
            comentario="Teste sem peso",
            instrucoes="Instrução de cardio",
            tempo_descanso_seg=0,
            is_composto=False,
            equipamento="Esteira",
            tipo_exercicio=TipoExercicio.SEM_PESO,
            sem_peso_details=SemPesoCreate(
                tempo_seg=1200.0,
                distancia_m=3000.0,
                calorias_estimadas=200.0,
                intensidade="moderada"
            )
        )
        
        created_1 = exercise_service.create_exercise(db, exercise_1)
        created_2 = exercise_service.create_exercise(db, exercise_2)
        
        return [created_1.id, created_2.id] 