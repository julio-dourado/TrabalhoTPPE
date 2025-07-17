from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, auth, training, exercises
from app.core.config import Settings

settings = Settings()

app = FastAPI(
    title="Training API",
    description="API for managing users and their training routines.",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    openapi_spec_args={
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Enter JWT token with 'Bearer ' prefix",
                }
            }
        },
        "security": [{"bearerAuth": []}],
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["exercises"])
app.include_router(training.router, prefix="/api/v1/training", tags=["training"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Training API!"}
