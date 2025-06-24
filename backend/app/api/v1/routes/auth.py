from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import Token
from app.services import user_service # Importa o serviço de usuário
from app.security.jwt import create_access_token # Importa create_access_token
from app.core.config import settings # Importa as configurações para tempo de expiração do token

router = APIRouter()

@router.post(
    "/token",
    response_model=Token,
    summary="Gera um token de acesso para autenticação"
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Valida as credenciais do usuário e retorna um token JWT de acesso.
    """
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciais inválidas"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id}, # Adiciona o ID do usuário ao token
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

