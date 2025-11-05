import re
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

PASSWORD_REGEX = r"^[a-zA-Z0-9]{1,72}$"
NAME_REGEX = r"^[а-яА-Яa-zA-Z]{1,50}$"


class AddUser(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    oauth_provider: Optional[str] = None


    @field_validator('name')
    def validator_name(cls, value: str):
        if not re.match(NAME_REGEX, value):
            raise ValueError(
                'name must contain only Cyrillic letters, Latin letters'
            )
        return value

    @field_validator('password')
    def validator_password(cls, value: str):
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                'password must contain only Latin letters and numbers'
            )
        return value


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