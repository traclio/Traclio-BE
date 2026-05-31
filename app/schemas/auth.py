from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    nickname: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserMeResponse(BaseModel):
    email: EmailStr
    nickname: str
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    profile_image: Optional[str] = None