# backend/app/routes/user.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import UserCreate, UserOut, User
from app.db.db import get_db
from app.services.user import create_user  # Importing the service function

router = APIRouter()

@router.post(
    "/user/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED  # agora retorna 201
)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.get(
    "/user/{user_id}",
    response_model=UserOut
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
