# Makefile para Crie Seu Treino - OTIMIZADO
# Comandos rápidos para Docker Compose

.PHONY: help build up down restart logs clean test test-backend test-all dev dev-fast dev-hot stop status

# Mostrar ajuda
help:
	@echo "🏋️  Crie Seu Treino - Comandos Otimizados:"
	@echo ""
	@echo "⚡ Desenvolvimento Rápido (Recomendado):"
	@echo "  make dev-fast   - Aplicação RÁPIDA (sem hot reload) - ⚡ 3x mais rápido!"
	@echo "  make dev        - Alias para dev-fast"
	@echo ""
	@echo "🔥 Desenvolvimento com Hot Reload:"
	@echo "  make dev-hot    - Com hot reload (mais lento no Windows)"
	@echo ""
	@echo "🚀 Controle de Serviços:"
	@echo "  make up         - Subir serviços (modo rápido)"
	@echo "  make down       - Parar todos os serviços"
	@echo "  make restart    - Reiniciar todos os serviços"
	@echo "  make stop       - Parar sem remover containers"
	@echo "  make status     - Ver status dos containers"
	@echo ""
	@echo "🧪 Testes:"
	@echo "  make test       - Rodar todos os testes (45 testes)"
	@echo "  make test-fast  - Testes backend rápidos"
	@echo ""
	@echo "🔧 Utilitários:"
	@echo "  make build      - Build de todos os containers"
	@echo "  make logs       - Ver logs em tempo real"
	@echo "  make clean      - Limpar tudo (containers + volumes)"
	@echo ""
	@echo "📱 Acesso:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend:  http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"

# Desenvolvimento rápido (padrão - sem hot reload, 3x mais rápido)
dev-fast: down
	@echo "⚡ Iniciando modo RÁPIDO (sem hot reload)..."
	@echo "   - Containers otimizados"
	@echo "   - Cache de build melhorado"
	@echo "   - Sem bind mounts (mais rápido no Windows)"
	docker-compose up --build -d
	@echo "✅ Aplicação rodando em modo RÁPIDO!"
	@echo "🎨 Frontend: http://localhost:3000"
	@echo "🚀 Backend:  http://localhost:8000"
	@echo "📚 API Docs: http://localhost:8000/docs"

# Alias para compatibilidade
dev: dev-fast

# Desenvolvimento com hot reload (mais lento mas permite edições)
dev-hot: down
	@echo "🔥 Iniciando modo DESENVOLVIMENTO (com hot reload)..."
	@echo "   - Hot reload habilitado"
	@echo "   - Bind mounts (pode ser lento no Windows)"
	docker-compose -f docker-compose.dev.yml up --build -d
	@echo "✅ Aplicação rodando com HOT RELOAD!"
	@echo "🎨 Frontend: http://localhost:3000 (auto-refresh)"
	@echo "🚀 Backend:  http://localhost:8000 (auto-reload)"
	@echo "💡 Edite os arquivos e veja as mudanças automaticamente!"

# Build todos os containers com cache otimizado
build:
	@echo "🔨 Building containers otimizados..."
	DOCKER_BUILDKIT=1 docker-compose build --parallel

# Subir todos os serviços (modo rápido)
up:
	@echo "🚀 Subindo serviços otimizados..."
	docker-compose up -d

# Parar todos os serviços
down:
	@echo "🛑 Parando serviços..."
	docker-compose down
	docker-compose -f docker-compose.dev.yml down 2>/dev/null || true

# Reiniciar tudo
restart: down
	@echo "🔄 Reiniciando..."
	$(MAKE) dev-fast

# Parar sem remover
stop:
	@echo "⏸️  Pausando serviços..."
	docker-compose stop
	docker-compose -f docker-compose.dev.yml stop 2>/dev/null || true

# Status dos containers
status:
	@echo "📊 Status dos containers:"
	docker-compose ps
	@echo ""
	@docker-compose -f docker-compose.dev.yml ps 2>/dev/null || true

# Ver logs em tempo real
logs:
	@echo "📄 Logs em tempo real (Ctrl+C para sair):"
	docker-compose logs -f

# Testes completos (45 testes)
test: down
	@echo "🧪 Executando TODOS os testes..."
	docker-compose --profile testing run --rm test-all
	@echo "✅ Testes concluídos!"

# Testes backend rápidos
test-fast: 
	@echo "⚡ Testes backend rápidos..."
	docker-compose --profile testing run --rm backend-test

# Limpeza completa
clean:
	@echo "🧹 Limpeza completa..."
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans 2>/dev/null || true
	docker system prune -f
	@echo "✅ Limpeza concluída!"

# Comandos avançados
shell-backend:
	@echo "🐚 Abrindo shell no backend..."
	docker-compose exec backend bash

shell-frontend:
	@echo "🐚 Abrindo shell no frontend..."
	docker-compose exec frontend sh

# Backup do banco
backup-db:
	@echo "💾 Fazendo backup do banco..."
	docker-compose exec db pg_dump -U user treino_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup salvo!" 