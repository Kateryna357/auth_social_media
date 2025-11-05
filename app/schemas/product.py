from pydantic import BaseModel


class AddProduct(BaseModel):
    name: str
    description: str
    price: int