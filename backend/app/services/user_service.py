from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User as SQLAlchemyUser
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.security.password import get_senha_hash, verify_password

def get_user_by_email(db: Session, email: str) -> Optional[SQLAlchemyUser]:
    """
    Obtém um usuário pelo endereço de e-mail.
    """
    return db.query(SQLAlchemyUser).filter(SQLAlchemyUser.email == email.lower()).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[SQLAlchemyUser]:
    """
    Autentica um usuário verificando o e-mail e a senha.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.senha_hash):
        return None
    return user

def create_user(db: Session, user: UserCreate) -> SQLAlchemyUser:
    """
    Cria um novo usuário no banco de dados.
    """
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este e-mail já existe."
        )
    
    hashed_password = get_senha_hash(user.senha)
    db_user = SQLAlchemyUser(
        nome=user.nome,
        email=user.email.lower(),
        senha_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: SQLAlchemyUser, user_update: UserUpdate) -> SQLAlchemyUser:
    """
    Atualiza os dados de um usuário existente.
    """
    if user_update.nome is not None:
        db_user.nome = user_update.nome
    if user_update.email is not None:
        db_user.email = user_update.email.lower()
    if user_update.senha is not None:
        db_user.senha_hash = get_senha_hash(user_update.senha)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: SQLAlchemyUser):
    """
    Deleta um usuário do banco de dados.
    """
    db.delete(db_user)
    db.commit()

