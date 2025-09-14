from typing import Optional

from pydantic import BaseModel, EmailStr


class AddUser(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    oauth_provider: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str