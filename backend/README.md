# Backend - API Crie Seu Treino

API REST construída com FastAPI para gerenciar usuários, treinos e exercícios.

## 🚀 Funcionalidades

- ✅ **Autenticação JWT**: Sistema completo de login/logout com tokens seguros
- ✅ **CRUD Usuários**: Registro, atualização e exclusão de contas
- ✅ **CRUD Treinos**: Criação e gerenciamento de treinos personalizados
- ✅ **CRUD Exercícios**: Exercícios com peso e sem peso
- ✅ **Segurança**: Autenticação por usuário com isolamento de dados
- ✅ **Banco PostgreSQL**: Persistência robusta com SQLAlchemy
- ✅ **Testes Completos**: Cobertura de testes de integração
- ✅ **Docker**: Containerização completa

## 📋 Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- PostgreSQL (se executar fora do Docker)

## 🔧 Como Executar

### Com Docker Compose (Recomendado)

```bash
# Subir todos os serviços
docker-compose up --build

# Apenas backend e banco
docker-compose up db backend --build

# Executar testes
docker-compose run backend-test
```

### Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/treino_db"
export SECRET_KEY="your-secret-key"

# Inicializar banco de dados
python -m app.init_db

# Executar aplicação
uvicorn app.main:app --reload

# Executar testes
./run_tests.sh
# ou
python -m pytest tests/ -v
```

## 📊 API Endpoints

### Autenticação
- `POST /auth/register` - Registrar novo usuário
- `POST /auth/login` - Fazer login
- `GET /auth/me` - Obter dados do usuário atual

### Usuários
- `GET /usuarios/` - Listar usuários
- `GET /usuarios/me/profile` - Perfil completo do usuário atual
- `PUT /usuarios/me` - Atualizar perfil
- `DELETE /usuarios/me` - Excluir conta

### Treinos
- `POST /treinos/` - Criar treino
- `GET /treinos/` - Listar meus treinos
- `GET /treinos/{id}` - Obter treino com exercícios
- `PUT /treinos/{id}` - Atualizar treino
- `DELETE /treinos/{id}` - Excluir treino

### Exercícios
- `POST /exercicios/treinos/{treino_id}/exercicios` - Criar exercício
- `GET /exercicios/treinos/{treino_id}/exercicios` - Listar exercícios do treino
- `GET /exercicios/{id}` - Obter exercício
- `PUT /exercicios/{id}` - Atualizar exercício
- `DELETE /exercicios/{id}` - Excluir exercício

## 🗂️ Estrutura do Projeto

```
backend/
├── app/
│   ├── auth/          # Sistema de autenticação JWT
│   ├── crud/          # Operações CRUD para cada entidade
│   ├── models/        # Modelos SQLAlchemy
│   ├── routers/       # Endpoints da API
│   ├── schemas/       # Schemas Pydantic para validação
│   ├── config.py      # Configurações da aplicação
│   ├── database.py    # Configuração do banco de dados
│   ├── main.py        # Aplicação FastAPI principal
│   └── init_db.py     # Script de inicialização do banco
├── tests/             # Testes de integração
├── requirements.txt   # Dependências Python
└── Dockerfile        # Container Docker
```

## 🔐 Segurança

- **JWT Tokens**: Autenticação segura com expiração
- **Hash de Senhas**: Bcrypt para armazenamento seguro
- **Isolamento de Dados**: Usuários só acessam seus próprios dados
- **Validação**: Pydantic para validação de entrada
- **CORS**: Configurado para frontend Next.js

## 🧪 Testes

Os testes cobrem:

- ✅ Autenticação (registro, login, tokens)
- ✅ CRUD de usuários
- ✅ CRUD de treinos
- ✅ CRUD de exercícios
- ✅ Segurança e isolamento de dados
- ✅ Casos de erro e edge cases

Execute com:

```bash
# Via Docker
docker-compose run backend-test

# Local
python -m pytest tests/ -v
```

## 🌐 URLs de Acesso

- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📦 Modelos de Dados

### Usuário
```json
{
  "nome": "string",
  "email": "email",
  "password": "string"
}
```

### Treino
```json
{
  "nome": "string",
  "descricao": "string (opcional)"
}
```

### Exercício Com Peso
```json
{
  "nome": "string",
  "tipo": "com_peso",
  "musculo": "string",
  "repeticoes": "integer",
  "sets": "integer", 
  "carga": "float"
}
```

### Exercício Sem Peso
```json
{
  "nome": "string",
  "tipo": "sem_peso",
  "tempo": "integer (segundos)",
  "distancia": "float (metros)"
}
``` 