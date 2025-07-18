#!/bin/bash

# Docker Scripts - Crie Seu Treino
# Scripts utilitários para gerenciar o ambiente Docker

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${2}${1}${NC}"
}

# Função para verificar se o Docker está rodando
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_message "Docker não está rodando. Por favor, inicie o Docker e tente novamente." $RED
        exit 1
    fi
}

# Função para verificar se o arquivo .env existe
check_env() {
    if [ ! -f .env ]; then
        print_message "Arquivo .env não encontrado. Criando um exemplo..." $YELLOW
        cat > .env << EOF
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=treino_db

# API
SECRET_KEY=sua_chave_secreta_muito_segura_aqui_com_pelo_menos_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENV=development
EOF
        print_message "Arquivo .env criado. Por favor, ajuste as configurações conforme necessário." $GREEN
    fi
}

# Função para iniciar ambiente de desenvolvimento
start_dev() {
    print_message "🚀 Iniciando ambiente de desenvolvimento..." $BLUE
    check_docker
    check_env
    docker-compose -f docker-compose.dev.yml up --build
}

# Função para iniciar ambiente de desenvolvimento em background
start_dev_bg() {
    print_message "🚀 Iniciando ambiente de desenvolvimento em background..." $BLUE
    check_docker
    check_env
    docker-compose -f docker-compose.dev.yml up -d --build
    print_message "✅ Serviços iniciados em background!" $GREEN
    print_message "📱 Frontend: http://localhost:3000" $BLUE
    print_message "🔗 Backend: http://localhost:8000" $BLUE
    print_message "🗄️  Database: localhost:5432" $BLUE
}

# Função para iniciar ambiente de produção
start_prod() {
    print_message "🏭 Iniciando ambiente de produção..." $BLUE
    check_docker
    check_env
    docker-compose --profile production up --build -d
    print_message "✅ Ambiente de produção iniciado!" $GREEN
    print_message "🌐 Frontend: http://localhost" $BLUE
    print_message "🔗 Backend: http://localhost:8000" $BLUE
}

# Função para parar todos os serviços
stop_all() {
    print_message "⏹️  Parando todos os serviços..." $YELLOW
    docker-compose -f docker-compose.dev.yml down
    docker-compose --profile production down
    docker-compose --profile test down
    print_message "✅ Todos os serviços parados!" $GREEN
}

# Função para executar testes
run_tests() {
    print_message "🧪 Executando testes do backend..." $BLUE
    check_docker
    check_env
    docker-compose --profile test up --build backend-test
}

# Função para ver logs
show_logs() {
    local service=${1:-""}
    if [ -z "$service" ]; then
        print_message "📋 Mostrando logs de todos os serviços de desenvolvimento..." $BLUE
        docker-compose -f docker-compose.dev.yml logs -f --tail=100
    else
        print_message "📋 Mostrando logs do serviço: $service" $BLUE
        docker-compose -f docker-compose.dev.yml logs -f --tail=100 "$service"
    fi
}

# Função para limpar containers e volumes
cleanup() {
    print_message "🧹 Limpando containers parados e volumes não utilizados..." $YELLOW
    docker-compose -f docker-compose.dev.yml down -v
    docker-compose --profile production down -v
    docker system prune -f
    print_message "✅ Limpeza concluída!" $GREEN
}

# Função para rebuild completo
rebuild() {
    print_message "🔄 Fazendo rebuild completo do ambiente..." $YELLOW
    stop_all
    docker-compose -f docker-compose.dev.yml build --no-cache
    start_dev_bg
    print_message "✅ Rebuild concluído!" $GREEN
}

# Função para mostrar status dos containers
status() {
    print_message "📊 Status dos containers:" $BLUE
    echo ""
    docker-compose -f docker-compose.dev.yml ps
    echo ""
    docker-compose --profile production ps
}

# Função para backup do banco de dados
backup_db() {
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    print_message "💾 Criando backup do banco de dados: $backup_file" $BLUE
    
    if docker-compose -f docker-compose.dev.yml ps | grep postgres_db_dev > /dev/null; then
        docker-compose -f docker-compose.dev.yml exec -T db pg_dump -U postgres treino_db > "$backup_file"
        print_message "✅ Backup criado: $backup_file" $GREEN
    else
        print_message "❌ Container do banco não está rodando!" $RED
        exit 1
    fi
}

# Função para restaurar backup do banco
restore_db() {
    local backup_file=$1
    if [ -z "$backup_file" ]; then
        print_message "❌ Por favor, especifique o arquivo de backup!" $RED
        print_message "Uso: $0 restore-db <arquivo_backup.sql>" $YELLOW
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_message "❌ Arquivo de backup não encontrado: $backup_file" $RED
        exit 1
    fi
    
    print_message "🔄 Restaurando backup do banco de dados: $backup_file" $BLUE
    docker-compose -f docker-compose.dev.yml exec -T db psql -U postgres treino_db < "$backup_file"
    print_message "✅ Backup restaurado!" $GREEN
}

# Função para mostrar ajuda
show_help() {
    echo "Docker Scripts - Crie Seu Treino"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  dev              Iniciar ambiente de desenvolvimento (interativo)"
    echo "  dev-bg           Iniciar ambiente de desenvolvimento (background)"
    echo "  prod             Iniciar ambiente de produção"
    echo "  stop             Parar todos os serviços"
    echo "  test             Executar testes do backend"
    echo "  logs [serviço]   Mostrar logs (todos ou de um serviço específico)"
    echo "  status           Mostrar status dos containers"
    echo "  cleanup          Limpar containers e volumes"
    echo "  rebuild          Rebuild completo do ambiente"
    echo "  backup-db        Criar backup do banco de dados"
    echo "  restore-db       Restaurar backup do banco de dados"
    echo "  help             Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 dev-bg        # Iniciar desenvolvimento em background"
    echo "  $0 logs frontend # Ver logs apenas do frontend"
    echo "  $0 backup-db     # Criar backup do banco"
    echo ""
}

# Menu principal
case ${1:-help} in
    "dev")
        start_dev
        ;;
    "dev-bg")
        start_dev_bg
        ;;
    "prod")
        start_prod
        ;;
    "stop")
        stop_all
        ;;
    "test")
        run_tests
        ;;
    "logs")
        show_logs $2
        ;;
    "status")
        status
        ;;
    "cleanup")
        cleanup
        ;;
    "rebuild")
        rebuild
        ;;
    "backup-db")
        backup_db
        ;;
    "restore-db")
        restore_db $2
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