from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    try:
        result = AuthService.login_user(db, login_data)
        return LoginResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/register", response_model=RegisterResponse)
def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        result = AuthService.register_user(db, register_data)
        return RegisterResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
