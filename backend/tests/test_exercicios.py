import pytest
from fastapi.testclient import TestClient
from app.models.exercicio import TipoExercicio


@pytest.fixture
def test_treino(client: TestClient, auth_headers):
    """Cria um treino para os testes de exercício"""
    treino_data = {
        "nome": "Treino para Exercícios",
        "descricao": "Treino usado nos testes de exercício"
    }
    response = client.post("/treinos/", headers=auth_headers, json=treino_data)
    return response.json()


def test_create_exercicio_com_peso(client: TestClient, auth_headers, test_treino):
    """Testa criação de exercício com peso"""
    exercicio_data = {
        "nome": "Supino Reto",
        "tipo": TipoExercicio.COM_PESO.value,
        "musculo": "Peitoral",
        "repeticoes": 12,
        "sets": 3,
        "carga": 80.5
    }
    treino_id = test_treino["id"]
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        headers=auth_headers,
        json=exercicio_data
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == exercicio_data["nome"]
    assert data["tipo"] == TipoExercicio.COM_PESO.value
    assert data["repeticoes"] == 12
    assert data["sets"] == 3
    assert data["carga"] == 80.5


def test_create_exercicio_sem_peso(client: TestClient, auth_headers, test_treino):
    """Testa criação de exercício sem peso"""
    exercicio_data = {
        "nome": "Corrida",
        "tipo": TipoExercicio.SEM_PESO.value,
        "tempo": 1800,  # 30 minutos em segundos
        "distancia": 5000  # 5 km em metros
    }
    treino_id = test_treino["id"]
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        headers=auth_headers,
        json=exercicio_data
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == exercicio_data["nome"]
    assert data["tipo"] == TipoExercicio.SEM_PESO.value
    assert data["tempo"] == 1800
    assert data["distancia"] == 5000


def test_create_exercicio_treino_inexistente(client: TestClient, auth_headers):
    """Testa criação de exercício em treino inexistente"""
    exercicio_data = {
        "nome": "Exercício Teste",
        "tipo": TipoExercicio.COM_PESO.value,
        "repeticoes": 10,
        "sets": 3,
        "carga": 50
    }
    response = client.post(
        "/exercicios/treinos/99999/exercicios",
        headers=auth_headers,
        json=exercicio_data
    )
    
    assert response.status_code == 404


def test_read_exercicios_by_treino(client: TestClient, auth_headers, test_treino):
    """Testa listagem de exercícios de um treino"""
    # Criar alguns exercícios primeiro
    exercicios_data = [
        {
            "nome": "Agachamento",
            "tipo": TipoExercicio.COM_PESO.value,
            "musculo": "Quadríceps",
            "repeticoes": 15,
            "sets": 4,
            "carga": 100
        },
        {
            "nome": "Flexão",
            "tipo": TipoExercicio.SEM_PESO.value,
            "tempo": 300
        }
    ]
    
    treino_id = test_treino["id"]
    for exercicio_data in exercicios_data:
        client.post(
            f"/exercicios/treinos/{treino_id}/exercicios",
            headers=auth_headers,
            json=exercicio_data
        )
    
    # Listar exercícios
    response = client.get(
        f"/exercicios/treinos/{treino_id}/exercicios",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["nome"] in ["Agachamento", "Flexão"]


def test_read_exercicio_by_id(client: TestClient, auth_headers, test_treino):
    """Testa busca de exercício por ID"""
    # Criar exercício
    exercicio_data = {
        "nome": "Rosca Bíceps",
        "tipo": TipoExercicio.COM_PESO.value,
        "musculo": "Bíceps",
        "repeticoes": 10,
        "sets": 3,
        "carga": 15
    }
    treino_id = test_treino["id"]
    create_response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        headers=auth_headers,
        json=exercicio_data
    )
    exercicio_id = create_response.json()["id"]
    
    # Buscar exercício
    response = client.get(f"/exercicios/{exercicio_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == exercicio_id
    assert data["nome"] == "Rosca Bíceps"


def test_update_exercicio(client: TestClient, auth_headers, test_treino):
    """Testa atualização de exercício"""
    # Criar exercício
    exercicio_data = {
        "nome": "Leg Press",
        "tipo": TipoExercicio.COM_PESO.value,
        "musculo": "Quadríceps",
        "repeticoes": 12,
        "sets": 3,
        "carga": 200
    }
    treino_id = test_treino["id"]
    create_response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        headers=auth_headers,
        json=exercicio_data
    )
    exercicio_id = create_response.json()["id"]
    
    # Atualizar exercício
    update_data = {
        "repeticoes": 15,
        "carga": 250
    }
    response = client.put(
        f"/exercicios/{exercicio_id}",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["repeticoes"] == 15
    assert data["carga"] == 250
    assert data["nome"] == "Leg Press"  # Nome não deve ter mudado


def test_delete_exercicio(client: TestClient, auth_headers, test_treino):
    """Testa exclusão de exercício"""
    # Criar exercício
    exercicio_data = {
        "nome": "Exercício para Deletar",
        "tipo": TipoExercicio.COM_PESO.value,
        "repeticoes": 10,
        "sets": 3,
        "carga": 50
    }
    treino_id = test_treino["id"]
    create_response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        headers=auth_headers,
        json=exercicio_data
    )
    exercicio_id = create_response.json()["id"]
    
    # Deletar exercício
    response = client.delete(f"/exercicios/{exercicio_id}", headers=auth_headers)
    
    assert response.status_code == 204
    
    # Verificar se foi deletado
    get_response = client.get(f"/exercicios/{exercicio_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_read_nonexistent_exercicio(client: TestClient, auth_headers):
    """Testa busca de exercício inexistente"""
    response = client.get("/exercicios/99999", headers=auth_headers)
    
    assert response.status_code == 404 