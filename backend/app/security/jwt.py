from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings

class TokenData:
    def __init__(self, user_id: Optional[int] = None):
        self.user_id = user_id

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um token JWT de acesso.
    Args:
        data (dict): Dados a serem codificados no token.
        expires_delta (Optional[timedelta]): Tempo de expiração do token. Se None, usa o padrão das settings.
    Returns:
        str: O token JWT codificado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[TokenData]:
    """
    Descodifica um token JWT e retorna os dados contidos nele.
    Args:
        token (str): O token JWT a ser descodificado.
    Returns:
        Optional[TokenData]: Um objeto TokenData se o token for válido, caso contrário None.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except JWTError:
        return None

