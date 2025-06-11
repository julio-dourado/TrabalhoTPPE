from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import Token
from app.services.user_service import authenticate_user
from app.security.jwt import create_access_token


router = APIRouter()


@router.post("/token", response_model=Token, summary="Gera um token de acesso")
def login_for_access_token(
    db: Session = Depends(get_db),

    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate_user(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"user_id": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}