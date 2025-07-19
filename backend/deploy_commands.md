# 🚀 Comandos para Deploy - Sistema Crie Seu Treino

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+ (para desenvolvimento local)
- Conta AWS (para deploy em produção)

## 🧪 1. Testes Locais

### Opção A: Docker Compose (Recomendado)

```bash
# 1. Clonar e entrar no diretório
cd "tppe 2"

# 2. Subir todos os serviços
docker-compose up --build -d

# 3. Verificar se está funcionando
curl http://localhost:8000/health

# 4. Testar API (opcional)
python backend/test_api.py

# 5. Executar testes
docker-compose run backend-test

# 6. Parar serviços
docker-compose down
```

### Opção B: Desenvolvimento Local

```bash
# 1. Entrar no backend
cd backend

# 2. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar banco (PostgreSQL local)
set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/treino_db
set SECRET_KEY=your-secret-key-here

# 5. Configurar banco de dados
python scripts/setup_database.py

# 6. Executar aplicação
uvicorn app.main:app --reload

# 7. Executar testes
python -m pytest tests/ -v
```

## 🗄️ 2. Banco de Dados Manual

### PostgreSQL Local

```bash
# 1. Conectar ao PostgreSQL
psql -U postgres

# 2. Criar banco
CREATE DATABASE treino_db;
\c treino_db;

# 3. Executar schema
\i backend/database/schema.sql

# 4. Inserir dados de teste (opcional)
\i backend/database/seed_data.sql
```

### Usando script Python

```bash
cd backend
python scripts/setup_database.py
```

## ☁️ 3. Deploy AWS - Preparação

### 3.1. Configurar AWS CLI

```bash
# Instalar AWS CLI
pip install awscli

# Configurar credenciais
aws configure
# AWS Access Key ID: [sua-key]
# AWS Secret Access Key: [sua-secret]
# Default region: us-east-1
# Default output format: json
```

### 3.2. Criar RDS PostgreSQL

```bash
# Via AWS CLI (exemplo)
aws rds create-db-instance \
    --db-instance-identifier treino-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 14.9 \
    --master-username postgres \
    --master-user-password SuaSenhaSegura123 \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --db-name treino_db \
    --backup-retention-period 7 \
    --storage-encrypted \
    --publicly-accessible
```

### 3.3. Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env para produção
cp backend/config/production.env backend/.env

# Editar com seus dados reais:
# DATABASE_URL=postgresql://postgres:SuaSenha@your-rds-endpoint:5432/treino_db
# SECRET_KEY=sua-chave-jwt-super-secreta-min-32-chars
```

## 🚀 4. Deploy AWS - Opções

### Opção A: AWS Elastic Beanstalk

```bash
# 1. Instalar EB CLI
pip install awsebcli

# 2. Inicializar aplicação
cd backend
eb init -p python-3.11 treino-api

# 3. Criar ambiente
eb create treino-prod --envvars \
    DATABASE_URL=postgresql://...,\
    SECRET_KEY=sua-chave,\
    ACCESS_TOKEN_EXPIRE_MINUTES=60

# 4. Deploy
eb deploy

# 5. Abrir no navegador
eb open
```

### Opção B: AWS ECS (Docker)

```bash
# 1. Fazer build da imagem
docker build -t treino-api ./backend

# 2. Tag para ECR
docker tag treino-api:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/treino-api:latest

# 3. Push para ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/treino-api:latest

# 4. Criar task definition e service via console ou CLI
```

### Opção C: EC2 com Docker

```bash
# 1. Conectar na instância EC2
ssh -i sua-chave.pem ec2-user@ip-da-instancia

# 2. Instalar Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# 3. Fazer upload do código
scp -i sua-chave.pem -r backend ec2-user@ip-da-instancia:~/

# 4. Configurar variáveis e rodar
cd backend
docker build -t treino-api .
docker run -d -p 8000:8000 --env-file .env treino-api
```

## 🧪 5. Validação e Testes

### Testar aplicação local

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Documentação
# Abra: http://localhost:8000/docs

# 3. Teste completo da API
python backend/test_api.py

# 4. Testes unitários
cd backend
python -m pytest tests/ -v
```

### Testar aplicação em produção

```bash
# 1. Health check
curl https://sua-url-aws.com/health

# 2. Teste com curl
curl -X POST https://sua-url-aws.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nome":"Test","email":"test@test.com","password":"123456"}'

# 3. Monitoramento de logs (Elastic Beanstalk)
eb logs
```

## 🔒 6. Segurança e Manutenção

### Backup do banco

```bash
# PostgreSQL dump
pg_dump -h your-rds-endpoint -U postgres treino_db > backup.sql

# Restore
psql -h your-rds-endpoint -U postgres treino_db < backup.sql
```

### Monitoramento

```bash
# Ver logs da aplicação
docker logs container-id

# Ver métricas (se usando CloudWatch)
aws logs describe-log-groups
```

### Atualizar aplicação

```bash
# Rebuild e redeploy
docker-compose build backend
docker-compose up -d backend

# Ou via Elastic Beanstalk
eb deploy
```

## ⚡ 7. Comandos Rápidos de Troubleshooting

```bash
# Ver logs dos containers
docker-compose logs backend

# Conectar no container
docker-compose exec backend bash

# Resetar banco de dados (CUIDADO!)
docker-compose down -v
docker-compose up --build

# Testar conexão com banco
python -c "from app.database import engine; print(engine.connect())"

# Ver todas as rotas disponíveis
curl http://localhost:8000/openapi.json | jq '.paths | keys'
```

## 📞 Suporte

Se algo não funcionar:

1. ✅ Verifique se o Docker está rodando
2. ✅ Confirme as variáveis de ambiente
3. ✅ Teste a conexão com o banco
4. ✅ Veja os logs: `docker-compose logs backend`
5. ✅ Execute os testes: `docker-compose run backend-test`

**URLs importantes:**
- **API Local**: http://localhost:8000
- **Docs**: http://localhost:8000/docs  
- **Health**: http://localhost:8000/health
- **Database**: localhost:5432 (se PostgreSQL local) 