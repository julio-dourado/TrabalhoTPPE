from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, get_user_by_email
from app.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()


# --- Rota Pública para CRIAR um usuário ---
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário"
)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este e-mail já existe.",
        )
    return create_user(db=db, user=user)


# --- ROTAS PROTEGIDAS ---
@router.get(
    "/me/",
    response_model=UserOut,
    summary="Obtém os dados do usuário autenticado"
)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user