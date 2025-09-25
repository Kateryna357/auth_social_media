from pydantic import BaseModel


class CheckPassword(BaseModel):
    password: str
