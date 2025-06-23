from fastapi import FastAPI
from app.api.v1.routes import users, auth, treino

app = FastAPI(
    title="Minha API de Treinos",
    description="API para gerenciar usuários e seus treinos.",
    version="0.1.0",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    openapi_spec_args={
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Insira o token JWT com o prefixo 'Bearer '",
                }
            }
        },
        "security": [{"bearerAuth": []}],
    },
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao sistema!"}

app.include_router(
    auth.router, 
    prefix="/api/v1/auth", 
    tags=["Authentication"]
)
app.include_router(
    users.router, 
    prefix="/api/v1/users", 
    tags=["Users"]
)
app.include_router(
    treino.router,
    prefix="/api/v1/treinos",
    tags=["Treinos"]
)
