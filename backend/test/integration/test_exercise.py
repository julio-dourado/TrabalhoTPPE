import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User as SQLAlchemyUser
from app.models.exercise import Exercicio, ComPeso, SemPeso
from app.models.training import Treino

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
            "serie": 4,
            "repeticoes": 8,
            "comentario": "Foco no peito",
            "tipo_exercicio": "ComPeso",
            "com_peso_details": {
                "peso": 80.0
            }
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Supino"
        assert data["serie"] == 4
        assert data["repeticoes"] == 8
        assert data["tipo_exercicio"] == "ComPeso"
        assert data["com_peso_details"]["peso"] == 80.0
        assert data["sem_peso_details"] is None
        assert "id" in data

    def test_create_exercise_sem_peso_success(self, client_with_db: TestClient):
        """
        US14: Teste de criação de exercício sem peso
        """
        exercise_data = {
            "nome": "Corrida",
            "serie": 1,
            "repeticoes": 1,
            "comentario": "Cardio matinal",
            "tipo_exercicio": "SemPeso",
            "sem_peso_details": {
                "tempo_seg": 1800.0,
                "distancia_m": 5000.0,
                "meta_velocidade": 2.78
            }
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Corrida"
        assert data["tipo_exercicio"] == "SemPeso"
        assert data["sem_peso_details"]["tempo_seg"] == 1800.0
        assert data["sem_peso_details"]["distancia_m"] == 5000.0
        assert data["sem_peso_details"]["meta_velocidade"] == 2.78
        assert data["com_peso_details"] is None

    def test_create_exercise_invalid_tipo(self, client_with_db: TestClient):
        """Teste de validação de tipo de exercício inválido"""
        exercise_data = {
            "nome": "Exercício Inválido",
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
            "serie": 4,
            "repeticoes": 8,
            "tipo_exercicio": "ComPeso"
            # Faltando com_peso_details
        }
        
        response = client_with_db.post("/api/v1/exercicios/", json=exercise_data)
        assert response.status_code == 422

    def test_create_exercise_sem_peso_without_details(self, client_with_db: TestClient):
        """Teste de validação: exercício sem peso sem detalhes"""
        exercise_data = {
            "nome": "Corrida",
            "serie": 1,
            "repeticoes": 1,
            "tipo_exercicio": "SemPeso"
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
        assert "ComPeso" in tipos
        assert "SemPeso" in tipos

    def test_get_exercises_by_type_com_peso(self, client_with_db: TestClient, db_session: Session):
        """Teste de filtragem por tipo ComPeso"""
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/?tipo=ComPeso")
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo_exercicio"] == "ComPeso" for ex in data)
        assert all(ex["com_peso_details"] is not None for ex in data)

    def test_get_exercises_by_type_sem_peso(self, client_with_db: TestClient, db_session: Session):
        """Teste de filtragem por tipo SemPeso"""
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/?tipo=SemPeso")
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo_exercicio"] == "SemPeso" for ex in data)
        assert all(ex["sem_peso_details"] is not None for ex in data)

    def test_get_exercises_invalid_type_filter(self, client_with_db: TestClient):
        """Teste de filtro com tipo inválido"""
        response = client_with_db.get("/api/v1/exercicios/?tipo=TipoInvalido")
        
        assert response.status_code == 400
        assert "Tipo deve ser 'ComPeso' ou 'SemPeso'" in response.json()["detail"]

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
                "peso": 90.0
            }
        }
        
        response = client_with_db.put(f"/api/v1/exercicios/{exercise_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Supino Atualizado"
        assert data["serie"] == 5
        assert data["com_peso_details"]["peso"] == 90.0

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
                "meta_velocidade": 2.5
            }
        }
        
        response = client_with_db.put(f"/api/v1/exercicios/{sem_peso_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Corrida Atualizada"
        assert data["sem_peso_details"]["tempo_seg"] == 2400.0
        assert data["sem_peso_details"]["distancia_m"] == 6000.0

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
        assert all(ex["tipo_exercicio"] == "ComPeso" for ex in data)
        assert all(ex["com_peso_details"] is not None for ex in data)

    def test_get_cardio_exercises_route(self, client_with_db: TestClient, db_session: Session):
        """Teste da rota específica para exercícios sem peso (cardio)"""
        self._create_test_exercises(db_session)
        
        response = client_with_db.get("/api/v1/exercicios/sem-peso/")
        
        assert response.status_code == 200
        data = response.json()
        assert all(ex["tipo_exercicio"] == "SemPeso" for ex in data)
        assert all(ex["sem_peso_details"] is not None for ex in data)

    def _create_test_exercises(self, db: Session) -> list[int]:
        """Helper para criar exercícios de teste"""
        # Limpar dados existentes
        db.query(ComPeso).delete()
        db.query(SemPeso).delete()
        db.query(Treino).delete()
        db.query(Exercicio).delete()
        
        # Exercício com peso
        exercicio_com_peso = Exercicio(
            nome="Supino Teste",
            serie=4,
            repeticoes=8,
            comentario="Teste",
            tipo_exercicio="ComPeso"
        )
        db.add(exercicio_com_peso)
        db.flush()
        
        com_peso = ComPeso(exercicio_id=exercicio_com_peso.id, peso=80.0)
        db.add(com_peso)
        
        # Exercício sem peso
        exercicio_sem_peso = Exercicio(
            nome="Corrida Teste",
            serie=1,
            repeticoes=1,
            comentario="Cardio teste",
            tipo_exercicio="SemPeso"
        )
        db.add(exercicio_sem_peso)
        db.flush()
        
        sem_peso = SemPeso(
            exercicio_id=exercicio_sem_peso.id,
            tempo_seg=1800.0,
            distancia_m=5000.0,
            meta_velocidade=2.78
        )
        db.add(sem_peso)
        
        db.commit()
        db.refresh(exercicio_com_peso)
        db.refresh(exercicio_sem_peso)
        
        return [exercicio_com_peso.id, exercicio_sem_peso.id] 