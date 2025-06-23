from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, get_user_by_email
from app.models.user import User
from app.api.v1.deps import get_current_user
from app.security.password import get_senha_hash

router = APIRouter()


# --- ROTAS PÚBLICAS ---
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário",
    response_model=UserOut,
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

@router.put(
    "/me/",
    response_model=UserOut,
    summary="Atualiza os dados do usuário autenticado"
)

@router.put(
    "/me/",
    response_model=UserOut,
    summary="Atualiza os dados do usuário autenticado"
)
def update_user_me(
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário autenticado não encontrado no banco de dados."
        )

    if user.email.lower() != db_user.email.lower():
        existing_email_user = get_user_by_email(db=db, email=user.email.lower())
        if existing_email_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um usuário com este novo e-mail já existe.",
            )

    db_user.nome = user.nome
    db_user.email = user.email.lower()

    if user.senha:
        db_user.senha_hash = get_senha_hash(user.senha)
                                        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.delete(
    "/me/",
    summary="Deleta o usuário autenticado",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db=db, email=current_user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    db.delete(db_user)
    db.commit()
    
    return {"detail": "Usuário deletado com sucesso."}