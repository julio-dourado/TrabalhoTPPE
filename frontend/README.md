# Training App Frontend

Frontend da aplicação de gerenciamento de treinos, desenvolvido com Next.js, TypeScript e Tailwind CSS.

## Tecnologias Utilizadas

- **Next.js 14** - Framework React para produção
- **TypeScript** - Superset do JavaScript com tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **Axios** - Cliente HTTP para requisições à API
- **Lucide React** - Ícones React

## Funcionalidades

- ✅ Tela inicial com status de conexão com o backend
- ✅ Interface moderna e responsiva
- ✅ Comunicação com a API do backend
- ✅ Configuração completa do Docker

## Estrutura do Projeto

```
frontend/
├── pages/
│   ├── _app.tsx          # Configuração do App
│   └── index.tsx         # Página inicial
├── services/
│   └── api.ts           # Configuração da API
├── styles/
│   └── globals.css      # Estilos globais
├── Dockerfile           # Configuração do Docker
└── package.json         # Dependências
```

## Como Executar

### Com Docker (Recomendado)

```bash
# Na raiz do projeto
docker-compose up --build
```

### Desenvolvimento Local

```bash
# Instalar dependências
npm install

# Executar em modo de desenvolvimento
npm run dev
```

A aplicação estará disponível em: http://localhost:3000

## Variáveis de Ambiente

- `API_URL`: URL do backend (padrão: http://localhost:8000)

## Próximos Passos

- [ ] Implementar autenticação
- [ ] Criar páginas para gerenciamento de usuários
- [ ] Implementar CRUD de exercícios
- [ ] Criar interface para treinos
- [ ] Adicionar testes unitários 