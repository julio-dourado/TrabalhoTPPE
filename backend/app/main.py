from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import engine
from .models import usuario, treino, exercicio
from .routers import auth, usuarios, treinos, exercicios


def create_tables():
    """Cria as tabelas no banco de dados"""
    usuario.Base.metadata.create_all(bind=engine)
    treino.Base.metadata.create_all(bind=engine)
    exercicio.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    create_tables()
    
    # Resolve forward references in schemas
    try:
        from .schemas import resolve_forward_references
        resolve_forward_references()
    except Exception:
        pass  # Continue even if schema resolution fails
    
    yield
    # Shutdown


# Criar instância da aplicação FastAPI
app = FastAPI(
    title="API Crie Seu Treino",
    description="API para gerenciar usuários, treinos e exercícios",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(treinos.router)
app.include_router(exercicios.router)


@app.get("/")
def read_root():
    """Endpoint raiz"""
    return {"message": "API Crie Seu Treino - Sistema de Gerenciamento de Treinos"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API funcionando corretamente"} 