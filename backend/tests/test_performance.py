"""
Testes básicos de performance da API
Verifica se os endpoints respondem em tempo hábil
"""

import pytest
import time
from fastapi.testclient import TestClient


def test_performance_endpoints_basicos(client: TestClient):
    """Testa performance dos endpoints básicos"""
    
    # Health check deve ser muito rápido
    start = time.time()
    response = client.get("/health")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 0.5  # Deve responder em menos de 500ms
    
    # Página principal
    start = time.time()
    response = client.get("/")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 1.0  # Deve responder em menos de 1s
    
    # OpenAPI JSON
    start = time.time()
    response = client.get("/openapi.json")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 2.0  # Pode demorar mais para gerar schema


def test_performance_autenticacao(client: TestClient):
    """Testa performance da autenticação"""
    
    # Registro deve ser razoavelmente rápido
    usuario_data = {
        "nome": "Performance Test",
        "email": "perf@test.com",
        "password": "123456"
    }
    
    start = time.time()
    response = client.post("/auth/register", json=usuario_data)
    duration = time.time() - start
    
    assert response.status_code == 201
    assert duration < 3.0  # Hash de senha pode demorar um pouco
    
    # Login deve ser rápido
    login_data = {
        "username": "perf@test.com",
        "password": "123456"
    }
    
    start = time.time()
    response = client.post("/auth/login", data=login_data)
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 2.0


def test_performance_crud_basico(client: TestClient, auth_headers):
    """Testa performance das operações CRUD básicas"""
    
    # Criar treino
    treino_data = {"nome": "Treino Performance", "descricao": "Teste"}
    
    start = time.time()
    response = client.post("/treinos/", json=treino_data, headers=auth_headers)
    duration = time.time() - start
    
    assert response.status_code == 201
    assert duration < 1.0
    treino_id = response.json()["id"]
    
    # Listar treinos
    start = time.time()
    response = client.get("/treinos/", headers=auth_headers)
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 1.0
    
    # Buscar treino específico
    start = time.time()
    response = client.get(f"/treinos/{treino_id}", headers=auth_headers)
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 1.0


def test_performance_multiplas_requisicoes(client: TestClient, auth_headers):
    """Testa performance com múltiplas requisições seguidas"""
    
    durations = []
    
    # Fazer 10 requisições seguidas ao health check
    for i in range(10):
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        durations.append(duration)
        
        assert response.status_code == 200
    
    # Verificar se as requisições se mantêm rápidas
    avg_duration = sum(durations) / len(durations)
    assert avg_duration < 0.3
    
    # Nenhuma requisição individual deve demorar muito
    max_duration = max(durations)
    assert max_duration < 1.0 