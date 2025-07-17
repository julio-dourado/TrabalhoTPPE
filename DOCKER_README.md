# Docker Setup - Crie Seu Treino

Este documento contém instruções para executar o sistema completo usando Docker.

## 🚀 Quick Start

### Pré-requisitos
- Docker e Docker Compose instalados
- Arquivo `.env` configurado (veja seção Configuração)

### Desenvolvimento (Recomendado)
```bash
# Subir todos os serviços para desenvolvimento
docker-compose -f docker-compose.dev.yml up --build

# Ou em background
docker-compose -f docker-compose.dev.yml up -d --build
```

### Produção
```bash
# Subir serviços de produção
docker-compose --profile production up --build

# Ou apenas o necessário para produção
docker-compose up db backend frontend-prod --build
```

## 📋 Serviços Disponíveis

### Desenvolvimento (`docker-compose.dev.yml`)
- **Database (PostgreSQL)**: `localhost:5432`
- **Backend (FastAPI)**: `localhost:8000`
- **Frontend (Vite Dev Server)**: `localhost:3000`

### Produção (`docker-compose.yml`)
- **Database (PostgreSQL)**: `localhost:2543`
- **Backend (FastAPI)**: `localhost:8000`
- **Frontend (Nginx)**: `localhost:80`

## ⚙️ Configuração

### 1. Arquivo `.env`
Crie um arquivo `.env` na raiz do projeto:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_DB=treino_db

# API
SECRET_KEY=sua_chave_secreta_muito_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENV=development
```

### 2. Variáveis de Ambiente do Frontend

O frontend usa as seguintes variáveis:
- `VITE_API_URL`: URL da API (configurada automaticamente no Docker)
- `NODE_ENV`: ambiente de execução

## 🛠️ Comandos Úteis

### Desenvolvimento
```bash
# Subir apenas o banco de dados
docker-compose -f docker-compose.dev.yml up db

# Subir backend e banco
docker-compose -f docker-compose.dev.yml up db backend

# Ver logs de um serviço específico
docker-compose -f docker-compose.dev.yml logs -f frontend

# Executar comandos no container
docker-compose -f docker-compose.dev.yml exec backend bash
docker-compose -f docker-compose.dev.yml exec frontend sh

# Parar todos os serviços
docker-compose -f docker-compose.dev.yml down

# Parar e remover volumes (CUIDADO: apaga dados do banco)
docker-compose -f docker-compose.dev.yml down -v
```

### Produção
```bash
# Build e start dos serviços de produção
docker-compose --profile production up --build -d

# Ver logs
docker-compose logs -f frontend-prod

# Parar serviços de produção
docker-compose --profile production down
```

### Testes
```bash
# Executar testes do backend
docker-compose --profile test up backend-test

# Ou com logs detalhados
docker-compose --profile test up --build backend-test
```

### Limpeza
```bash
# Remover containers parados
docker-compose down

# Remover imagens não utilizadas
docker image prune

# Limpeza completa (CUIDADO)
docker system prune -a
```

## 🏗️ Estrutura dos Containers

### Backend Container
- **Base**: Python 3.11
- **Porta**: 8000
- **Hot Reload**: Ativado em desenvolvimento
- **Volumes**: Código fonte montado para desenvolvimento

### Frontend Container
- **Desenvolvimento**: Node.js 18 Alpine + Vite Dev Server
- **Produção**: Nginx Alpine servindo build estático
- **Porta**: 5173 (dev) / 80 (prod)
- **Hot Reload**: Ativado em desenvolvimento

### Database Container
- **Base**: PostgreSQL 15
- **Porta**: 5432 (dev) / 2543 (prod)
- **Persistência**: Volume Docker
- **Inicialização**: Scripts SQL automáticos

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco de dados**
   ```bash
   # Verificar se o banco está rodando
   docker-compose -f docker-compose.dev.yml ps
   
   # Ver logs do banco
   docker-compose -f docker-compose.dev.yml logs db
   ```

2. **Frontend não carrega**
   ```bash
   # Verificar se o Vite está rodando corretamente
   docker-compose -f docker-compose.dev.yml logs frontend
   
   # Rebuild do frontend
   docker-compose -f docker-compose.dev.yml up --build frontend
   ```

3. **API não responde**
   ```bash
   # Verificar logs do backend
   docker-compose -f docker-compose.dev.yml logs backend
   
   # Entrar no container para debug
   docker-compose -f docker-compose.dev.yml exec backend bash
   ```

4. **Problemas de permissão (Linux/Mac)**
   ```bash
   # Ajustar permissões dos volumes
   sudo chown -R $USER:$USER ./backend
   sudo chown -R $USER:$USER ./frontend
   ```

5. **Cache de dependências**
   ```bash
   # Rebuild forçando pull de imagens
   docker-compose -f docker-compose.dev.yml build --no-cache
   
   # Remover volumes de node_modules
   docker volume prune
   ```

### Monitoramento

```bash
# Ver status de todos os containers
docker-compose -f docker-compose.dev.yml ps

# Ver uso de recursos
docker stats

# Ver logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f --tail=100
```

## 🚀 Deploy

### Para Ambiente de Produção

1. **Configure as variáveis de ambiente de produção**
2. **Use o docker-compose de produção**
3. **Configure um reverse proxy (nginx/traefik) se necessário**
4. **Configure SSL/TLS**
5. **Configure backup do banco de dados**

```bash
# Exemplo de deploy simples
docker-compose --profile production up -d --build

# Com backup do banco
docker-compose exec db pg_dump -U postgres treino_db > backup.sql
```

## 📚 Links Úteis

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vite Documentation](https://vitejs.dev/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

## 🆘 Suporte

Se você encontrar problemas:

1. Verifique os logs dos containers
2. Consulte a seção de troubleshooting
3. Verifique se todas as dependências estão instaladas
4. Abra uma issue no repositório com logs detalhados 