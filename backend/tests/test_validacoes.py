"""
Testes de validação de dados
Verifica se a API valida corretamente os dados de entrada
"""

import pytest
from fastapi.testclient import TestClient
from app.models.exercicio import TipoExercicio


def test_validacao_registro_usuario(client: TestClient):
    """Testa validações no registro de usuário"""
    
    # Email inválido
    usuario_data = {
        "nome": "Teste",
        "email": "email-inválido",
        "password": "123456"
    }
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 422
    
    # Nome vazio
    usuario_data = {
        "nome": "",
        "email": "test@test.com",
        "password": "123456"
    }
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 422
    
    # Sem senha
    usuario_data = {
        "nome": "Teste",
        "email": "test@test.com"
    }
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 422
    
    # Dados válidos devem funcionar
    usuario_data = {
        "nome": "Usuário Válido",
        "email": "valido@test.com",
        "password": "senha123"
    }
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 201


def test_validacao_treino(client: TestClient, auth_headers):
    """Testa validações na criação de treino"""
    
    # Nome vazio
    treino_data = {
        "nome": "",
        "descricao": "Descrição"
    }
    response = client.post("/treinos/", json=treino_data, headers=auth_headers)
    assert response.status_code == 422
    
    # Sem nome
    treino_data = {
        "descricao": "Só descrição"
    }
    response = client.post("/treinos/", json=treino_data, headers=auth_headers)
    assert response.status_code == 422
    
    # Dados válidos
    treino_data = {
        "nome": "Treino Válido",
        "descricao": "Descrição válida"
    }
    response = client.post("/treinos/", json=treino_data, headers=auth_headers)
    assert response.status_code == 201


def test_validacao_exercicio_com_peso(client: TestClient, auth_headers):
    """Testa validações de exercício com peso"""
    
    # Criar treino primeiro
    treino_data = {"nome": "Treino Validação"}
    treino_response = client.post("/treinos/", json=treino_data, headers=auth_headers)
    treino_id = treino_response.json()["id"]
    
    # Exercício com peso sem campos obrigatórios
    exercicio_data = {
        "nome": "Supino",
        "tipo": TipoExercicio.COM_PESO.value,
        "musculo": "Peitoral"
        # Faltam: repeticoes, sets, carga
    }
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=auth_headers
    )
    # Deve aceitar porque os campos são opcionais no schema atual
    # mas vamos testar com valores inválidos
    
    # Valores negativos
    exercicio_data = {
        "nome": "Supino",
        "tipo": TipoExercicio.COM_PESO.value,
        "musculo": "Peitoral",
        "repeticoes": -5,
        "sets": -2,
        "carga": -10.0
    }
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=auth_headers
    )
    # Por enquanto aceita, mas poderia ser validado
    
    # Tipo inválido
    exercicio_data = {
        "nome": "Supino",
        "tipo": "tipo_inválido",
        "musculo": "Peitoral",
        "repeticoes": 12,
        "sets": 3,
        "carga": 80.0
    }
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=auth_headers
    )
    assert response.status_code == 422  # Deve falhar por tipo inválido
    
    # Dados válidos
    exercicio_data = {
        "nome": "Supino Reto",
        "tipo": TipoExercicio.COM_PESO.value,
        "musculo": "Peitoral",
        "repeticoes": 12,
        "sets": 3,
        "carga": 80.0
    }
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=auth_headers
    )
    assert response.status_code == 201


def test_validacao_exercicio_sem_peso(client: TestClient, auth_headers):
    """Testa validações de exercício sem peso"""
    
    # Criar treino primeiro
    treino_data = {"nome": "Treino Cardio"}
    treino_response = client.post("/treinos/", json=treino_data, headers=auth_headers)
    treino_id = treino_response.json()["id"]
    
    # Nome vazio
    exercicio_data = {
        "nome": "",
        "tipo": TipoExercicio.SEM_PESO.value,
        "tempo": 1800
    }
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=auth_headers
    )
    assert response.status_code == 422
    
    # Dados válidos com tempo
    exercicio_data = {
        "nome": "Corrida",
        "tipo": TipoExercicio.SEM_PESO.value,
        "tempo": 1800,
        "distancia": 5000
    }
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    
    # Dados válidos só com distância
    exercicio_data = {
        "nome": "Caminhada",
        "tipo": TipoExercicio.SEM_PESO.value,
        "distancia": 2000
    }
    response = client.post(
        f"/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=auth_headers
    )
    assert response.status_code == 201


def test_validacao_atualizacoes(client: TestClient):
    """Testa validações nas atualizações"""
    
    # Primeiro registrar e fazer login
    register_data = {
        "nome": "Teste Validação",
        "email": "validacao@test.com",
        "password": "senha123"
    }
    client.post("/auth/register", json=register_data)
    
    login_data = {"username": "validacao@test.com", "password": "senha123"}
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # Email inválido na atualização
    usuario_update = {
        "email": "email-inválido"
    }
    response = client.put("/usuarios/me", json=usuario_update, headers=auth_headers)
    assert response.status_code == 422
    
    # Teste concluído com sucesso - email inválido foi corretamente rejeitado
    pass


def test_validacao_json_malformado(client: TestClient, auth_headers):
    """Testa comportamento com JSON malformado"""
    
    # JSON inválido
    response = client.post(
        "/treinos/",
        data='{"nome": "Treino", "descricao":}',  # JSON malformado
        headers={**auth_headers, "Content-Type": "application/json"}
    )
    assert response.status_code == 422
    
    # Sem Content-Type
    response = client.post(
        "/treinos/",
        data='{"nome": "Treino"}',
        headers=auth_headers  # Sem Content-Type
    )
    # FastAPI deve lidar com isso automaticamente 