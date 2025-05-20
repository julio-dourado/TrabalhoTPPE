# backend/app/models/user.py

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, Integer, String
from app.db.db import Base

class User(Base):
    __tablename__ = 'usuarios'

    id            = Column(Integer, primary_key=True, index=True)
    nome          = Column(String, index=True)
    email         = Column(String, unique=True, index=True)
    senha_hash = Column(String)

class UserCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    nome: str
    email: str
    class Config:
        orm_mode = True
