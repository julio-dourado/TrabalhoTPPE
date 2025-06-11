from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.services.user_service import create_user
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

@router.post(
    "/user/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Usuário criado com sucesso"},
        400: {"description": "Email já cadastrado"},
        422: {"description": "Dados inválidos"}
    }
)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(user, db)
    except HTTPException as he:
        # Captura exceções específicas lançadas pelo serviço
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no servidor: {str(e)}"
        )