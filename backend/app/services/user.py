from sqlalchemy.orm import Session
from app.models.user import User, UserCreate
from fastapi import HTTPException

def create_user(user: UserCreate, db: Session) -> User:
    # Checking if the user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    

    db_user = User(nome=user.nome, email=user.email, senha_hash=user.senha)
    
    # Adding to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
