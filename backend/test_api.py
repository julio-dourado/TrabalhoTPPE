"""
Script de teste manual da API para demonstração
Execute após subir a aplicação com docker-compose up
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testando API Crie Seu Treino...")
    
    # 1. Registrar usuário
    print("\n1. Registrando usuário...")
    user_data = {
        "nome": "João Silva",
        "email": "joao@exemplo.com",
        "password": "senha123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code == 201:
        print("✅ Usuário registrado com sucesso!")
        user = response.json()
        print(f"   ID: {user['id']}, Nome: {user['nome']}")
    else:
        print(f"❌ Erro ao registrar: {response.status_code}")
        return

    # 2. Fazer login
    print("\n2. Fazendo login...")
    login_data = {
        "username": "joao@exemplo.com",
        "password": "senha123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        print("✅ Login realizado com sucesso!")
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print(f"❌ Erro no login: {response.status_code}")
        return

    # 3. Criar treino
    print("\n3. Criando treino...")
    treino_data = {
        "nome": "Treino Push",
        "descricao": "Treino de empurrar - peito, ombro e tríceps"
    }
    
    response = requests.post(f"{BASE_URL}/treinos/", json=treino_data, headers=headers)
    if response.status_code == 201:
        print("✅ Treino criado com sucesso!")
        treino = response.json()
        treino_id = treino["id"]
        print(f"   ID: {treino_id}, Nome: {treino['nome']}")
    else:
        print(f"❌ Erro ao criar treino: {response.status_code}")
        return

    # 4. Criar exercício com peso
    print("\n4. Criando exercício com peso...")
    exercicio_data = {
        "nome": "Supino Reto",
        "tipo": "com_peso",
        "musculo": "Peitoral",
        "repeticoes": 12,
        "sets": 3,
        "carga": 80.5
    }
    
    response = requests.post(
        f"{BASE_URL}/exercicios/treinos/{treino_id}/exercicios",
        json=exercicio_data,
        headers=headers
    )
    if response.status_code == 201:
        print("✅ Exercício com peso criado!")
        exercicio = response.json()
        print(f"   {exercicio['nome']}: {exercicio['sets']}x{exercicio['repeticoes']} - {exercicio['carga']}kg")
    else:
        print(f"❌ Erro ao criar exercício: {response.status_code}")

    # 5. Criar exercício sem peso
    print("\n5. Criando exercício sem peso...")
    cardio_data = {
        "nome": "Corrida",
        "tipo": "sem_peso",
        "tempo": 1800,  # 30 minutos
        "distancia": 5000  # 5km
    }
    
    response = requests.post(
        f"{BASE_URL}/exercicios/treinos/{treino_id}/exercicios",
        json=cardio_data,
        headers=headers
    )
    if response.status_code == 201:
        print("✅ Exercício sem peso criado!")
        cardio = response.json()
        print(f"   {cardio['nome']}: {cardio['tempo']}s - {cardio['distancia']}m")
    else:
        print(f"❌ Erro ao criar exercício: {response.status_code}")

    # 6. Listar treinos
    print("\n6. Listando treinos...")
    response = requests.get(f"{BASE_URL}/treinos/", headers=headers)
    if response.status_code == 200:
        treinos = response.json()
        print(f"✅ {len(treinos)} treino(s) encontrado(s)")
        for t in treinos:
            print(f"   - {t['nome']}: {t['descricao']}")
    else:
        print(f"❌ Erro ao listar treinos: {response.status_code}")

    # 7. Obter treino com exercícios
    print("\n7. Obtendo treino completo...")
    response = requests.get(f"{BASE_URL}/treinos/{treino_id}", headers=headers)
    if response.status_code == 200:
        treino_completo = response.json()
        print("✅ Treino completo:")
        print(f"   Nome: {treino_completo['nome']}")
        print(f"   Exercícios: {len(treino_completo['exercicios'])}")
        for ex in treino_completo['exercicios']:
            print(f"   - {ex['nome']} ({ex['tipo']})")
    else:
        print(f"❌ Erro ao obter treino: {response.status_code}")

    print("\n🎉 Teste da API concluído com sucesso!")
    print("📖 Acesse a documentação em: http://localhost:8000/docs")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("   Certifique-se de que o backend está rodando em http://localhost:8000")
        print("   Execute: docker-compose up backend")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}") 