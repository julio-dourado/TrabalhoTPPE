from fastapi import FastAPI
from app.api.v1.routes import users 
from app.db.session import init_db  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base

app = FastAPI()

DATABASE_URL = "postgresql://appuser:secret@db:5432/appdb"

# Conectar ao banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao sistema!"}
