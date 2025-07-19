from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.usuario import UsuarioCreate, Usuario, Token
from ..crud.usuario import create_usuario, get_usuario_by_email
from ..auth.auth import authenticate_user, create_access_token, get_current_active_user
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def register_user(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra novo usuário"""
    # Verifica se email já existe
    db_user = get_usuario_by_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email já está registrado"
        )
    
    return create_usuario(db=db, usuario=usuario)


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Faz login e retorna token JWT"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=Usuario)
def read_users_me(current_user: Usuario = Depends(get_current_active_user)):
    """Retorna dados do usuário atual"""
    return current_user 