from datetime import timedelta

from authlib.integrations.base_client import OAuthError
from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from app.core.config import settings
from app.core.security import create_access_token
from app.services.user import registration, auth_user, get_user_email
from app.db.session import get_db
from app.schemas.user import AddUser, UserOut, Token, UserLogin
from app.utils.google import oauth

router = APIRouter()


@router.post("/user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def user_registration(add: AddUser, db: Session = Depends(get_db)):
    user = registration(db, add)
    return user


@router.post('/token', response_model=Token)
async def login(user_db: UserLogin, db: Session = Depends(get_db)):
    user = auth_user(db, user_db.email, user_db.password)
    if not user:
        raise HTTPException(status_code=400, detail='incorrect email or password')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user_db.email},
        expires_delta=access_token_expires
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@router.get("/auth/google/login")
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URL
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        prompt="select_account"
    )


@router.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        print(request.url)
        token = await oauth.google.authorize_access_token(request)
        print(request.url)
        resp = await oauth.google.get("userinfo", token=token)
        user_info = resp.json()
    except OAuthError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="oauth failed"
        )

    email = user_info.get("email")
    name = user_info.get("name")

    user = get_user_email(db, email)
    if not user:
        user_create = AddUser(
            email=email,
            password=None,
            name=name,
            oauth_provider="google"
        )
        user = registration(db, user_create)

    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email
    })

    return {"access_token": access_token}




