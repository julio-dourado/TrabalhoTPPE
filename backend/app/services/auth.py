from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.utils.config import settings

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=3)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
