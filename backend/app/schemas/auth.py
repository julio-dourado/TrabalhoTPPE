from typing import Optional
from pydantic import BaseModel

# JWT Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None