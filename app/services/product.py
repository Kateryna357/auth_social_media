from sqlalchemy.orm import Session

from app.models.data import Product
from app.schemas.product import AddProduct


def add_product(db: Session, add: AddProduct) -> Product:
    products = Product(**add.model_dump())
    db.add(products)
    db.commit()
    db.refresh(products)
    return products




