"""
Testes de integração completos da API
Testa todo o fluxo: registro -> login -> criar treino -> adicionar exercícios -> consultar dados
"""

import pytest
from fastapi.testclient import TestClient
from app.models.exercicio import TipoExercicio


class TestIntegracaoCompleta:
    """Teste de integração que simula o uso real da API"""
    
    def test_fluxo_completo_usuario(self, client: TestClient):
        """Testa o fluxo completo de um usuário usando a API"""
        
        # 1. REGISTRO DE USUÁRIO
        usuario_data = {
            "nome": "João Silva",
            "email": "joao.teste@email.com",
            "password": "senha123"
        }
        
        response = client.post("/auth/register", json=usuario_data)
        assert response.status_code == 201
        user = response.json()
        assert user["nome"] == usuario_data["nome"]
        assert user["email"] == usuario_data["email"]
        assert "id" in user
        user_id = user["id"]
        
        # 2. LOGIN
        login_data = {
            "username": "joao.teste@email.com",
            "password": "senha123"
        }
        
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        # Headers para requisições autenticadas
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        
        # 3. VERIFICAR DADOS DO USUÁRIO ATUAL
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        current_user = response.json()
        assert current_user["email"] == usuario_data["email"]
        assert current_user["id"] == user_id
        
        # 4. CRIAR TREINO
        treino_data = {
            "nome": "Treino Push",
            "descricao": "Treino de peitoral, ombros e tríceps"
        }
        
        response = client.post("/treinos/", json=treino_data, headers=headers)
        assert response.status_code == 201
        treino = response.json()
        assert treino["nome"] == treino_data["nome"]
        assert treino["descricao"] == treino_data["descricao"]
        assert treino["usuario_id"] == user_id
        treino_id = treino["id"]
        
        # 5. ADICIONAR EXERCÍCIO COM PESO
        exercicio_peso = {
            "nome": "Supino Reto",
            "tipo": TipoExercicio.COM_PESO.value,
            "musculo": "Peitoral",
            "repeticoes": 12,
            "sets": 3,
            "carga": 80.0
        }
        
        response = client.post(
            f"/exercicios/treinos/{treino_id}/exercicios",
            json=exercicio_peso,
            headers=headers
        )
        assert response.status_code == 201
        exercicio = response.json()
        assert exercicio["nome"] == exercicio_peso["nome"]
        assert exercicio["tipo"] == TipoExercicio.COM_PESO.value
        assert exercicio["repeticoes"] == 12
        assert exercicio["carga"] == 80.0
        exercicio_peso_id = exercicio["id"]
        
        # 6. ADICIONAR EXERCÍCIO SEM PESO
        exercicio_cardio = {
            "nome": "Corrida",
            "tipo": TipoExercicio.SEM_PESO.value,
            "tempo": 1800,  # 30 minutos
            "distancia": 5000  # 5km
        }
        
        response = client.post(
            f"/exercicios/treinos/{treino_id}/exercicios",
            json=exercicio_cardio,
            headers=headers
        )
        assert response.status_code == 201
        cardio = response.json()
        assert cardio["nome"] == exercicio_cardio["nome"]
        assert cardio["tipo"] == TipoExercicio.SEM_PESO.value
        assert cardio["tempo"] == 1800
        assert cardio["distancia"] == 5000.0
        exercicio_cardio_id = cardio["id"]
        
        # 7. LISTAR EXERCÍCIOS DO TREINO
        response = client.get(f"/exercicios/treinos/{treino_id}/exercicios", headers=headers)
        assert response.status_code == 200
        exercicios = response.json()
        assert len(exercicios) == 2
        nomes_exercicios = [ex["nome"] for ex in exercicios]
        assert "Supino Reto" in nomes_exercicios
        assert "Corrida" in nomes_exercicios
        
        # 8. LISTAR TREINOS DO USUÁRIO
        response = client.get("/treinos/", headers=headers)
        assert response.status_code == 200
        treinos = response.json()
        assert len(treinos) == 1
        assert treinos[0]["nome"] == "Treino Push"
        
        # 9. BUSCAR TREINO ESPECÍFICO
        response = client.get(f"/treinos/{treino_id}", headers=headers)
        assert response.status_code == 200
        treino_detalhado = response.json()
        assert treino_detalhado["nome"] == "Treino Push"
        assert treino_detalhado["id"] == treino_id
        
        # 10. ATUALIZAR EXERCÍCIO
        exercicio_update = {
            "carga": 85.0,
            "repeticoes": 10
        }
        
        response = client.put(
            f"/exercicios/{exercicio_peso_id}",
            json=exercicio_update,
            headers=headers
        )
        assert response.status_code == 200
        exercicio_atualizado = response.json()
        assert exercicio_atualizado["carga"] == 85.0
        assert exercicio_atualizado["repeticoes"] == 10
        assert exercicio_atualizado["nome"] == "Supino Reto"  # Nome não deve mudar
        
        # 11. ATUALIZAR TREINO
        treino_update = {
            "nome": "Treino Push Atualizado",
            "descricao": "Descrição atualizada"
        }
        
        response = client.put(f"/treinos/{treino_id}", json=treino_update, headers=headers)
        assert response.status_code == 200
        treino_atualizado = response.json()
        assert treino_atualizado["nome"] == "Treino Push Atualizado"
        assert treino_atualizado["descricao"] == "Descrição atualizada"
        
        # 12. ATUALIZAR PERFIL DO USUÁRIO
        usuario_update = {
            "nome": "João Silva Santos"
        }
        
        response = client.put("/usuarios/me", json=usuario_update, headers=headers)
        assert response.status_code == 200
        usuario_atualizado = response.json()
        assert usuario_atualizado["nome"] == "João Silva Santos"
        assert usuario_atualizado["email"] == "joao.teste@email.com"
        
        # 13. BUSCAR EXERCÍCIO ESPECÍFICO
        response = client.get(f"/exercicios/{exercicio_peso_id}", headers=headers)
        assert response.status_code == 200
        exercicio_buscado = response.json()
        assert exercicio_buscado["nome"] == "Supino Reto"
        assert exercicio_buscado["carga"] == 85.0
        
        # 14. DELETAR EXERCÍCIO
        response = client.delete(f"/exercicios/{exercicio_cardio_id}", headers=headers)
        assert response.status_code == 204
        
        # Verificar se foi deletado
        response = client.get(f"/exercicios/{exercicio_cardio_id}", headers=headers)
        assert response.status_code == 404
        
        # 15. DELETAR TREINO (deve deletar exercícios restantes também)
        response = client.delete(f"/treinos/{treino_id}", headers=headers)
        assert response.status_code == 204
        
        # Verificar se foi deletado
        response = client.get(f"/treinos/{treino_id}", headers=headers)
        assert response.status_code == 404
        
        # Verificar se exercício também foi deletado (CASCADE)
        response = client.get(f"/exercicios/{exercicio_peso_id}", headers=headers)
        assert response.status_code == 404
        
        # 16. DELETAR CONTA DO USUÁRIO
        response = client.delete("/usuarios/me", headers=headers)
        assert response.status_code == 204
        
        # Verificar se não consegue mais acessar
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401


def test_todos_endpoints_basicos(client: TestClient):
    """Testa endpoints básicos da aplicação"""
    
    # Health check
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    
    # Página principal
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # OpenAPI JSON
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi = response.json()
    assert "openapi" in openapi
    assert "paths" in openapi


def test_erros_de_autenticacao(client: TestClient):
    """Testa cenários de erro de autenticação"""
    
    # Tentar acessar endpoint protegido sem token
    response = client.get("/usuarios/")
    assert response.status_code == 401
    
    response = client.get("/treinos/")
    assert response.status_code == 401
    
    response = client.get("/auth/me")
    assert response.status_code == 401
    
    # Login com credenciais inválidas
    login_data = {
        "username": "usuario@inexistente.com",
        "password": "senhaerrada"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    
    # Registrar email duplicado
    usuario_data = {
        "nome": "Usuário 1",
        "email": "duplicado@test.com",
        "password": "123456"
    }
    
    # Primeiro registro
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 201
    
    # Segundo registro com mesmo email
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 400


def test_erros_de_recursos_nao_encontrados(client: TestClient, auth_headers):
    """Testa cenários de recursos não encontrados"""
    
    # Buscar usuário inexistente
    response = client.get("/usuarios/99999", headers=auth_headers)
    assert response.status_code == 404
    
    # Buscar treino inexistente
    response = client.get("/treinos/99999", headers=auth_headers)
    assert response.status_code == 404
    
    # Buscar exercício inexistente  
    response = client.get("/exercicios/99999", headers=auth_headers)
    assert response.status_code == 404
    
    # Criar exercício em treino inexistente
    exercicio_data = {
        "nome": "Teste",
        "tipo": "com_peso",
        "repeticoes": 10,
        "sets": 3,
        "carga": 50
    }
    response = client.post("/exercicios/treinos/99999/exercicios", json=exercicio_data, headers=auth_headers)
    assert response.status_code == 404


def test_isolamento_entre_usuarios(client: TestClient, db):
    """Testa que usuários não podem acessar dados de outros usuários"""
    
    # Criar dois usuários
    user1_data = {"nome": "User 1", "email": "user1@test.com", "password": "123456"}
    user2_data = {"nome": "User 2", "email": "user2@test.com", "password": "123456"}
    
    # Registrar usuários
    client.post("/auth/register", json=user1_data)
    client.post("/auth/register", json=user2_data)
    
    # Login user1
    login1 = client.post("/auth/login", data={"username": "user1@test.com", "password": "123456"})
    token1 = login1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    
    # Login user2  
    login2 = client.post("/auth/login", data={"username": "user2@test.com", "password": "123456"})
    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # User1 cria treino
    treino_data = {"nome": "Treino do User1"}
    response = client.post("/treinos/", json=treino_data, headers=headers1)
    treino_id = response.json()["id"]
    
    # User2 tenta acessar treino do User1 (deve falhar)
    response = client.get(f"/treinos/{treino_id}", headers=headers2)
    assert response.status_code == 404
    
    # User2 não deve ver treinos do User1 na listagem
    response = client.get("/treinos/", headers=headers2)
    assert response.status_code == 200
    treinos = response.json()
    assert len(treinos) == 0 