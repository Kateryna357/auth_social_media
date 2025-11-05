from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.services.product import add_product
from app.db.session import get_db
from app.schemas.product import AddProduct

router = APIRouter()



@router.post('/add')
def add_products(add: AddProduct, db: Session = Depends(get_db)):
    add_product(db, add)
    return JSONResponse(content={'message': 'product added successfully'})