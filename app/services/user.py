from typing import Union, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import AddUser


def registration(db: Session, add: AddUser) -> User:
    existing_user = db.query(User).filter(User.email == add.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    user = User(
        email=add.email,
        hashed_password=get_password_hash(add.password),
        name=add.name,
        oauth_provider=add.oauth_provider
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def auth_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def get_user_email(db: Session, email: str):
    return db.query(User).filter(email=email).first()