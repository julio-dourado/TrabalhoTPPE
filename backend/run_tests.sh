#!/bin/bash

echo "🧪 Executando testes de integração..."

# Criar banco de teste se não existir
export DATABASE_URL="sqlite:///./test.db"
export SECRET_KEY="test-secret-key"
export ACCESS_TOKEN_EXPIRE_MINUTES=30

# Executar testes
python -m pytest tests/ -v --tb=short

# Limpar arquivo de teste
rm -f test.db

echo "✅ Testes concluídos!" 