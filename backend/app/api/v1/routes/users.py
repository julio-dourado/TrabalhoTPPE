from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service # Importa o serviço de usuário
from app.models.user import User as SQLAlchemyUser
from app.api.v1.deps import get_current_user
from app.security.password import get_senha_hash # Usado para hashing na rota de update, se aplicável

router = APIRouter()

# --- ROTAS PÚBLICAS ---
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário",
    response_model=UserOut,
)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)

# --- ROTAS PROTEGIDAS ---
@router.get(
    "/me/",
    response_model=UserOut,
    summary="Obtém os dados do usuário autenticado"
)
def read_users_me(current_user: SQLAlchemyUser = Depends(get_current_user)):
    return current_user

@router.put(
    "/me/",
    response_model=UserOut,
    summary="Atualiza os dados do usuário autenticado"
)
def update_user_me(
    user_update: UserUpdate, # Renomeado para evitar conflito com UserCreate
    current_user: SQLAlchemyUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Obtém o usuário do DB
    db_user = user_service.get_user_by_email(db=db, email=current_user.email)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário autenticado não encontrado no banco de dados."
        )

    # Verifica se o novo e-mail já existe e não pertence ao usuário atual
    if user_update.email is not None and user_update.email.lower() != db_user.email.lower():
        existing_email_user = user_service.get_user_by_email(db=db, email=user_update.email.lower())
        if existing_email_user and existing_email_user.id != db_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um usuário com este novo e-mail já existe.",
            )

    return user_service.update_user(db=db, db_user=db_user, user_update=user_update)

@router.delete(
    "/me/",
    summary="Deleta o usuário autenticado",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_me(
    current_user: SQLAlchemyUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = user_service.get_user_by_email(db=db, email=current_user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    user_service.delete_user(db=db, db_user=db_user)
    return # Retorna 204 No Content

