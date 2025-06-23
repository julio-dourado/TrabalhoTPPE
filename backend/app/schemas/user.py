from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    nome: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    senha: str = Field(..., min_length=6, description="A senha do usuário")


class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=6, description="A nova senha do usuário")


class UserOut(UserBase):
    id: int
    model_config = ConfigDict(
        from_attributes=True,
    )