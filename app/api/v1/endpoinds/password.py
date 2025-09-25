from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.utils.password import validate_password
from app.schemas.password import CheckPassword

router = APIRouter()


@router.post('/validate')
def check_validated_password(data: CheckPassword):
    if not validate_password(data.password):
        return JSONResponse(status_code=200, content={'message': 'password is correct'})
    else:
        return validate_password(data.password)