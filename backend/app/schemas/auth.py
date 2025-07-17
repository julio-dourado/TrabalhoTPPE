from pydantic import BaseModel, Field, EmailStr

# Login request schema


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")


# Login response schema
class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(
        default="bearer", description="Token type (always 'bearer')"
    )
    user_id: int = Field(..., description="User ID")


# Token data for internal use
class TokenData(BaseModel):
    email: str = Field(..., description="User email from token")
    user_id: int = Field(..., description="User ID from token")


# User registration request schema
class UserRegistrationRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="User name")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    password_confirm: str = Field(
        ..., min_length=8, description="Password confirmation"
    )


# Password change request schema
class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    new_password_confirm: str = Field(
        ..., min_length=8, description="New password confirmation"
    )


# Password reset request schema
class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")


# Password reset confirm schema
class PasswordResetConfirm(BaseModel):
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=8, description="New password")
    new_password_confirm: str = Field(
        ..., min_length=8, description="New password confirmation"
    )
