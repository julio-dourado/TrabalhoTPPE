from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate
from app.utils.security import get_senha_hash, verify_senha
from typing import Optional

def create_user(user: UserCreate, db: Session) -> User:
    try:
        existing_user = db.query(User).filter(
            User.email.ilike(user.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado",
                headers={"X-Error-Detail": "DuplicateEmail"}
            )

        hashed_password = get_senha_hash(user.senha)
        
        db_user = User(
            nome=user.nome.strip(),
            email=user.email.lower(),
            senha_hash=hashed_password
        )
    
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    except HTTPException:
        raise
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

def get_user_by_email(email: str, db: Session) -> Optional[User]:

    return db.query(User).filter(User.email.ilike(email)).first()

def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    user = get_user_by_email(email, db)
    
    if not user:
        return None

    if not verify_senha(password, user.senha_hash):
        return None
        
    return user

def get_user(user_id: int, db: Session) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()