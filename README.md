# Trabalho de TPPE

### Aqui se encontram as minhas refatorações, correções e novas funcionalidades do projeto "Crie Seu Treino" para a disciplina de POO

## 🎯 Objetivos

- ✅ Adicionar novos requisitos.
- ✅ Prototipar a solução.
- ✅ Criar uma arquitetura diferente de MVC.
- ✅ Criar Pipelines.
- ✅ Fazer Testes Unitários.
- ✅ Adicionar lint.
- ✅ Seguir a pep8.
- ✅ Criar uma persistência de dados em banco.
- ✅ Criar um ambiente de desenvolvimento virtualizado (Docker).

---

## 📋 Estrutura de Requisitos

### Épicos e Features

| Épico | Descrição                            |
| ----- | ------------------------------------ |
| E01   | Gestão de Conta do Usuário           |
| E02   | Gestão de Treinos e Exercícios       |
| E03   | Visualização e Interação com Treinos |

| Feature | Descrição               |
| ------- | ----------------------- |
| FT01    | Conta do Usuário        |
| FT02    | Treinos                 |
| FT03    | Exercícios com Peso     |
| FT04    | Exercícios sem Peso     |
| FT05    | Visualização de Treinos |

---

## 📊 Backlog do Produto

| Épico | Feature | US   | Descrição                                                                                                    | Status |
| ----- | ------- | ---- | ------------------------------------------------------------------------------------------------------------ | ------ |
| E01   | FT01    | US01 | Eu, como usuário, gostaria de me registrar no sistema.                                                       | ✅      |
| E01   | FT01    | US02 | Eu, como usuário, gostaria de fazer login no sistema.                                                        | ✅      |
| E01   | FT01    | US03 | Eu, como usuário, gostaria de fazer logout da minha conta.                                                   | ✅      |
| E01   | FT01    | US04 | Eu, como usuário, gostaria de visualizar meus dados da conta.                                                | ✅      |
| E01   | FT01    | US05 | Eu, como usuário, gostaria de editar meus dados da conta.                                                    | ✅      |
| E01   | FT01    | US06 | Eu, como usuário, gostaria de excluir minha conta.                                                           | ✅      |
| E02   | FT02    | US07 | Eu, como usuário, gostaria de criar um treino com exercícios personalizados.                                 | ✅      |
| E02   | FT02    | US08 | Eu, como usuário, gostaria de visualizar os treinos criados.                                                 | ✅      |
| E02   | FT02    | US09 | Eu, como usuário, gostaria de editar um treino existente.                                                    | ✅      |
| E02   | FT02    | US10 | Eu, como usuário, gostaria de excluir um treino.                                                             | ✅      |
| E02   | FT03    | US11 | Eu, como usuário, gostaria de criar exercícios com peso, informando nome, músculo, repetições, sets e carga. | ✅      |
| E02   | FT03    | US12 | Eu, como usuário, gostaria de editar exercícios com peso.                                                    | ✅      |
| E02   | FT03    | US13 | Eu, como usuário, gostaria de excluir exercícios com peso.                                                   | ✅      |
| E02   | FT04    | US14 | Eu, como usuário, gostaria de criar exercícios sem peso, informando nome, tempo e distância.                 | ✅      |
| E02   | FT04    | US15 | Eu, como usuário, gostaria de editar exercícios sem peso.                                                    | ✅      |
| E02   | FT04    | US16 | Eu, como usuário, gostaria de excluir exercícios sem peso.                                                   | ✅      |
| E03   | FT05    | US17 | Eu, como usuário, gostaria de visualizar uma lista de treinos e selecionar um para ver os detalhes.          | ✅      |
| E03   | FT05    | US18 | Eu, como usuário, gostaria de visualizar os detalhes de um treino com todos os exercícios listados.          | ✅      |

---

## 🏗️ Arquitetura do Sistema

Este projeto segue uma arquitetura de microsserviços com:

### Backend (API) 🚀
- **FastAPI** - Framework web Python moderno e rápido
- **PostgreSQL** - Banco de dados relacional robusto
- **SQLAlchemy** - ORM para Python com relacionamentos
- **JWT** - Autenticação segura via tokens
- **Pytest** - Testes unitários e de integração (45 testes passando!)
- **Docker** - Containerização para desenvolvimento

### Frontend (Web) 🎨
- **Next.js 14** - Framework React com App Router
- **TypeScript** - Tipagem estática para maior segurança
- **TailwindCSS** - Framework CSS utilitário moderno
- **Axios** - Cliente HTTP para comunicação com a API
- **Design responsivo** - Funciona perfeitamente em desktop e mobile

### Containerização 🐳
- **Docker** - Containerização dos serviços
- **Docker Compose** - Orquestração dos containers
- **Makefile** - Comandos rápidos para desenvolvimento

---

## 🚀 Como Executar

### ⚡ Método Super Rápido (Recomendado)

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd tppe2

# Rodar TUDO com um comando (backend + frontend + banco)
make dev
```

**Pronto! 🎉** Aplicação completa rodando em:
- **🎨 Frontend**: http://localhost:3000
- **🚀 Backend**: http://localhost:8000  
- **📚 API Docs**: http://localhost:8000/docs

### 🎯 Comandos Rápidos

```bash
# Ver todos os comandos disponíveis
make help

# Desenvolvimento
make dev          # Rodar aplicação completa
make up           # Subir serviços 
make down         # Parar serviços
make restart      # Reiniciar tudo

# Testes
make test         # Rodar todos os 45 testes
make test-fast    # Testes rápidos backend

# Utilitários  
make logs         # Ver logs
make clean        # Limpar tudo
make status       # Status dos containers
```

### 📦 Método Manual (Docker Compose)

```bash
# Rodar aplicação completa
docker-compose up --build -d

# Rodar apenas backend + banco
docker-compose up db backend -d

# Executar testes
docker-compose --profile testing run --rm test-all
```

### 🌐 Acessar os serviços

- **🎨 Frontend (Aplicação Principal)**: http://localhost:3000
- **🚀 Backend API**: http://localhost:8000
- **📚 Documentação da API**: http://localhost:8000/docs
- **🐘 PostgreSQL**: localhost:5432

### 🧪 Executar testes

```bash
# Método rápido
make test

# Ou método manual
docker-compose --profile testing run --rm backend-test

# Resultado esperado: 45 passed ✅
```

---

## 🎨 Interface do Frontend

O frontend foi desenvolvido inspirado no protótipo do Figma com:

- **🎨 Design moderno** com cor primária #8F93FF
- **📱 Responsivo** para todos os dispositivos
- **⚡ Navegação fluida** entre páginas
- **🔐 Autenticação segura** com JWT
- **✨ Animações suaves** com Tailwind

### 📄 Páginas principais:

1. **Login/Registro** - Autenticação com visual isométrico
2. **Dashboard** - Visão geral dos treinos e estatísticas
3. **Treinos** - Lista e gerenciamento de treinos
4. **Detalhes do Treino** - Exercícios com formulário dinâmico
5. **Perfil** - Dados pessoais e configurações

---

## 🧪 Qualidade e Testes

### ✅ Cobertura de Testes (45 testes passando)

- **🔐 Autenticação**: 7 testes
  - Registro, login, JWT validation
- **👥 Usuários**: 8 testes  
  - CRUD completo, perfil, isolamento
- **💪 Treinos**: 7 testes
  - CRUD, visualização, segurança
- **🏋️ Exercícios**: 8 testes
  - Criação com/sem peso, validações
- **🔄 Integração**: 5 testes
  - Fluxos completos end-to-end
- **⚡ Performance**: 4 testes
  - Carga e velocidade
- **✅ Validações**: 6 testes
  - Dados inválidos, edge cases

### 📊 Resultado dos Testes
```
=============================== 45 passed, 9 warnings in 43.29s ===============================
```

---

## 🛠️ Desenvolvimento

### Comandos Docker Compose

```bash
# Ver status dos containers
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Entrar no container do backend
docker-compose exec backend bash

# Entrar no container do frontend
docker-compose exec frontend sh

# Reconstruir containers
docker-compose up --build
```

### Estrutura de Containers

```yaml
📦 Aplicação
├── 🐘 PostgreSQL (db) - Porta 5432
├── 🚀 Backend (FastAPI) - Porta 8000  
├── 🎨 Frontend (Next.js) - Porta 3000
└── 🧪 Testes (pytest) - On demand
```

---

## 🗄️ Banco de Dados

### Estrutura:
- **Usuários** - Dados pessoais e autenticação
- **Treinos** - Nome, descrição, relacionamento com usuário  
- **Exercícios** - Com peso (repetições, sets, carga) ou sem peso (tempo, distância)

### Relacionamentos:
- Usuario 1:N Treino
- Treino 1:N Exercicio

---

## 🚢 Deploy e Produção

### Variáveis de Ambiente
```bash
# Backend
DATABASE_URL=postgresql://user:password@db:5432/treino_db
SECRET_KEY=your-super-secret-jwt-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database
POSTGRES_DB=treino_db
POSTGRES_USER=user  
POSTGRES_PASSWORD=password
```

### Deploy AWS
```bash
# Script automatizado disponível
python scripts/deploy_aws.py
```

---

## 🎯 Funcionalidades Implementadas

### ✅ Autenticação Completa
- Registro e login seguros
- JWT tokens com expiração
- Middleware de autenticação
- Logout automático

### ✅ Gestão de Treinos
- Criar, editar, excluir treinos
- Visualização em cards responsivos
- Dashboard com estatísticas
- Isolamento por usuário

### ✅ Sistema de Exercícios
- Exercícios com peso (repetições, sets, carga)
- Exercícios sem peso (tempo, distância)
- Interface intuitiva para criação
- Cards com todas as informações

### ✅ Interface Moderna  
- Design inspirado no Figma
- Cor primária #8F93FF
- Animações e transições
- Mobile-first responsivo

### ✅ Integração Completa
- Frontend integrado 100% com backend
- Tratamento de erros
- Loading states
- Validações em tempo real

### ✅ DevOps Simplificado
- Docker Compose completo
- Makefile com comandos rápidos
- Testes automatizados
- Build otimizado para produção

---

## 🔧 Troubleshooting

### Problemas Comuns

**Frontend não conecta com backend:**
```bash
# Verificar se backend está rodando
make status
# Reiniciar se necessário
make restart
```

**Banco de dados com erro:**
```bash
# Limpar e recriar
make clean
make dev
```

**Testes falhando:**
```bash
# Executar testes isolados
make test-fast
```

**Porta em uso:**
```bash
# Parar todos os serviços
make down
# Ou matar processos nas portas
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

---

## 📈 Próximos Passos

- [ ] Sistema de notificações
- [ ] Histórico de treinos realizados  
- [ ] Gráficos de progresso
- [ ] Compartilhamento de treinos
- [ ] App mobile nativo
- [ ] CI/CD automatizado
- [ ] Monitoramento com Prometheus

---

## 🏆 Resultados Alcançados

✨ **Sistema completo e funcional** com todas as user stories implementadas  
🎯 **45 testes passando** garantindo qualidade do código  
🎨 **Interface moderna** seguindo o protótipo do Figma  
🔐 **Segurança robusta** com JWT e validações  
🚀 **Deploy fácil** com Docker e scripts automatizados  
📱 **Experiência mobile** otimizada para todos os dispositivos  
⚡ **Desenvolvimento rápido** com comandos Make simplificados  

---

**Desenvolvido com ❤️ para a disciplina de TPPE**
