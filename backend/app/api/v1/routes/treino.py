from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from app.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.get(
    "/me/",
    response_model=UserOut,
    summary="Obtém os dados do usuário autenticado"
)
def read_me_trains(current_user: User = Depends(get_current_user)):
    return current_user