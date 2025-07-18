#!/bin/bash

# Training App - Deploy Script
# Script para automatizar o deployment da aplicação

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
COMPOSE_FILE_DEV="docker-compose.dev.yml"
COMPOSE_FILE_PROD="docker-compose.prod.yml"
BACKUP_DIR="/opt/backups"

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${2}${1}${NC}"
}

# Função para verificar se o Docker está rodando
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_message "❌ Docker não está rodando. Por favor, inicie o Docker e tente novamente." $RED
        exit 1
    fi
}

# Função para verificar se o arquivo .env existe
check_env() {
    local env_file=${1:-".env"}
    if [ ! -f "$env_file" ]; then
        print_message "❌ Arquivo $env_file não encontrado!" $RED
        print_message "📋 Copie o arquivo environment.example para $env_file e configure as variáveis." $YELLOW
        exit 1
    fi
}

# Função para criar backup do banco de dados
create_backup() {
    local compose_file=$1
    local backup_name="backup-$(date +%Y%m%d-%H%M%S).sql.gz"
    
    print_message "💾 Criando backup do banco de dados..." $BLUE
    
    if [ -f "$compose_file" ]; then
        mkdir -p "$BACKUP_DIR"
        if docker-compose -f "$compose_file" exec -T db pg_dump -U postgres training_db | gzip > "$BACKUP_DIR/$backup_name"; then
            print_message "✅ Backup criado: $BACKUP_DIR/$backup_name" $GREEN
        else
            print_message "⚠️  Falha ao criar backup, continuando mesmo assim..." $YELLOW
        fi
    fi
}

# Função para verificar saúde dos serviços
check_health() {
    local compose_file=$1
    
    print_message "🔍 Verificando saúde dos serviços..." $BLUE
    
    # Aguardar alguns segundos para os serviços subirem
    sleep 10
    
    # Verificar se os containers estão rodando
    if docker-compose -f "$compose_file" ps | grep -q "Up"; then
        print_message "✅ Containers estão rodando!" $GREEN
    else
        print_message "❌ Alguns containers não estão rodando corretamente." $RED
        docker-compose -f "$compose_file" ps
        exit 1
    fi
    
    # Verificar health checks
    if command -v curl >/dev/null 2>&1; then
        print_message "🔍 Testando endpoints..." $BLUE
        
        # Testar backend
        if curl -f http://localhost:8000/health >/dev/null 2>&1; then
            print_message "✅ Backend respondendo corretamente!" $GREEN
        else
            print_message "⚠️  Backend não está respondendo no health check." $YELLOW
        fi
        
        # Testar frontend (apenas em produção)
        if [ "$compose_file" = "$COMPOSE_FILE_PROD" ]; then
            if curl -f http://localhost/health >/dev/null 2>&1; then
                print_message "✅ Frontend respondendo corretamente!" $GREEN
            else
                print_message "⚠️  Frontend não está respondendo no health check." $YELLOW
            fi
        fi
    fi
}

# Função para deploy de desenvolvimento
deploy_dev() {
    print_message "🚀 Iniciando deploy de desenvolvimento..." $BLUE
    
    check_docker
    check_env
    
    # Parar serviços existentes
    print_message "⏹️  Parando serviços existentes..." $YELLOW
    docker-compose -f "$COMPOSE_FILE_DEV" down
    
    # Subir serviços
    print_message "🏗️  Construindo e subindo serviços..." $BLUE
    docker-compose -f "$COMPOSE_FILE_DEV" up -d --build
    
    # Verificar saúde
    check_health "$COMPOSE_FILE_DEV"
    
    print_message "✅ Deploy de desenvolvimento concluído!" $GREEN
    print_message "🌐 Frontend: http://localhost:3000" $BLUE
    print_message "🔗 Backend: http://localhost:8000" $BLUE
    print_message "📚 API Docs: http://localhost:8000/docs" $BLUE
}

# Função para deploy de produção
deploy_prod() {
    print_message "🏭 Iniciando deploy de produção..." $BLUE
    
    check_docker
    check_env ".env.prod"
    
    # Criar backup antes do deploy
    create_backup "$COMPOSE_FILE_PROD"
    
    # Parar serviços existentes
    print_message "⏹️  Parando serviços existentes..." $YELLOW
    docker-compose -f "$COMPOSE_FILE_PROD" down
    
    # Subir serviços
    print_message "🏗️  Construindo e subindo serviços de produção..." $BLUE
    docker-compose -f "$COMPOSE_FILE_PROD" up -d --build
    
    # Verificar saúde
    check_health "$COMPOSE_FILE_PROD"
    
    print_message "✅ Deploy de produção concluído!" $GREEN
    print_message "🌐 Frontend: http://localhost" $BLUE
    print_message "🔗 Backend: http://localhost:8000" $BLUE
    print_message "📚 API Docs: http://localhost:8000/docs" $BLUE
}

# Função para atualização sem downtime
rolling_update() {
    local service=${1:-"backend"}
    print_message "🔄 Fazendo rolling update do serviço: $service" $BLUE
    
    check_docker
    check_env ".env.prod"
    
    # Atualizar apenas o serviço especificado
    docker-compose -f "$COMPOSE_FILE_PROD" up -d --no-deps --build "$service"
    
    # Verificar saúde
    check_health "$COMPOSE_FILE_PROD"
    
    print_message "✅ Rolling update do $service concluído!" $GREEN
}

# Função para parar todos os serviços
stop_all() {
    print_message "⏹️  Parando todos os serviços..." $YELLOW
    
    docker-compose -f "$COMPOSE_FILE_DEV" down 2>/dev/null || true
    docker-compose -f "$COMPOSE_FILE_PROD" down 2>/dev/null || true
    
    print_message "✅ Todos os serviços parados!" $GREEN
}

# Função para mostrar logs
show_logs() {
    local compose_file=${1:-"$COMPOSE_FILE_DEV"}
    local service=${2:-""}
    
    print_message "📋 Mostrando logs..." $BLUE
    
    if [ -z "$service" ]; then
        docker-compose -f "$compose_file" logs -f --tail=100
    else
        docker-compose -f "$compose_file" logs -f --tail=100 "$service"
    fi
}

# Função para mostrar status
show_status() {
    local compose_file=${1:-"$COMPOSE_FILE_DEV"}
    
    print_message "📊 Status dos serviços:" $BLUE
    docker-compose -f "$compose_file" ps
    
    print_message "💻 Uso de recursos:" $BLUE
    docker stats --no-stream
}

# Função para executar testes
run_tests() {
    print_message "🧪 Executando testes..." $BLUE
    
    check_docker
    check_env
    
    # Executar testes do backend
    docker-compose -f "$COMPOSE_FILE_DEV" run --rm backend pytest
    
    print_message "✅ Testes concluídos!" $GREEN
}

# Função para limpeza
cleanup() {
    print_message "🧹 Limpando recursos não utilizados..." $YELLOW
    
    # Parar todos os serviços
    stop_all
    
    # Remover containers parados
    docker container prune -f
    
    # Remover imagens não utilizadas
    docker image prune -f
    
    # Remover volumes não utilizados (cuidado com dados)
    read -p "Deseja remover volumes não utilizados? (CUIDADO: pode apagar dados) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f
    fi
    
    print_message "✅ Limpeza concluída!" $GREEN
}

# Função para mostrar ajuda
show_help() {
    echo "🚀 Training App - Deploy Script"
    echo ""
    echo "Uso: $0 [comando] [opções]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  dev                 Deploy de desenvolvimento"
    echo "  prod                Deploy de produção"
    echo "  stop                Parar todos os serviços"
    echo "  logs [dev|prod]     Mostrar logs"
    echo "  status [dev|prod]   Mostrar status dos serviços"
    echo "  test                Executar testes"
    echo "  update [service]    Rolling update (produção)"
    echo "  backup              Criar backup do banco"
    echo "  cleanup             Limpeza de recursos"
    echo "  help                Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 dev              # Deploy de desenvolvimento"
    echo "  $0 prod             # Deploy de produção"
    echo "  $0 logs prod        # Ver logs de produção"
    echo "  $0 update backend   # Atualizar apenas backend"
    echo "  $0 backup           # Criar backup"
    echo ""
    echo "Arquivos necessários:"
    echo "  .env                # Variáveis de ambiente (desenvolvimento)"
    echo "  .env.prod           # Variáveis de ambiente (produção)"
    echo ""
}

# Menu principal
case ${1:-help} in
    "dev")
        deploy_dev
        ;;
    "prod")
        deploy_prod
        ;;
    "stop")
        stop_all
        ;;
    "logs")
        if [ "$2" = "prod" ]; then
            show_logs "$COMPOSE_FILE_PROD" "$3"
        else
            show_logs "$COMPOSE_FILE_DEV" "$3"
        fi
        ;;
    "status")
        if [ "$2" = "prod" ]; then
            show_status "$COMPOSE_FILE_PROD"
        else
            show_status "$COMPOSE_FILE_DEV"
        fi
        ;;
    "test")
        run_tests
        ;;
    "update")
        rolling_update "$2"
        ;;
    "backup")
        create_backup "$COMPOSE_FILE_PROD"
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        print_message "❌ Comando não reconhecido: $1" $RED
        echo ""
        show_help
        exit 1
        ;;
esac 