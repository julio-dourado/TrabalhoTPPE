#!/usr/bin/env python3
"""Script para debugar problema de criação de exercício"""

from fastapi.testclient import TestClient
from app.main import app
import json

def test_exercise_creation():
    client = TestClient(app)
    
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
    
    print("Dados enviados:")
    print(json.dumps(exercise_data, indent=2))
    
    response = client.post("/api/v1/exercicios/", json=exercise_data)
    
    print(f"\nStatus Code: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
    except:
        print(f"Response text: {response.text}")
    
    if response.status_code != 201:
        print("\n❌ Erro na criação do exercício!")
        return False
    else:
        print("\n✅ Exercício criado com sucesso!")
        return True

if __name__ == "__main__":
    test_exercise_creation() 