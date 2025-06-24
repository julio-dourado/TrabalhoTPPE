#!/usr/bin/env python3
"""Script para aplicar migração no banco de dados"""

import sqlite3
import os

def apply_migration():
    db_path = 'test.db'
    migration_path = 'migrations/update_schema.sql'
    
    if not os.path.exists(migration_path):
        print(f"Arquivo de migração não encontrado: {migration_path}")
        return False
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        
        # Ler e executar a migração
        with open(migration_path, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        # Executar as mudanças em uma transação
        conn.executescript(migration_sql)
        conn.commit()
        conn.close()
        
        print("✅ Migração aplicada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao aplicar migração: {e}")
        return False

if __name__ == "__main__":
    apply_migration() 