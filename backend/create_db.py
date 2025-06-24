#!/usr/bin/env python3
"""Script para criar o banco de dados do zero"""

import sqlite3
import os

def create_database():
    db_path = 'test.db'
    schema_path = 'migrations/create_schema.sql'
    
    # Remover banco existente se houver
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Banco existente removido: {db_path}")
    
    if not os.path.exists(schema_path):
        print(f"Arquivo de schema não encontrado: {schema_path}")
        return False
    
    try:
        # Conectar ao banco (será criado automaticamente)
        conn = sqlite3.connect(db_path)
        
        # Ler e executar o schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Executar as mudanças
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
        
        print("✅ Banco de dados criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

if __name__ == "__main__":
    create_database() 