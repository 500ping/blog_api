from typing import Any
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import bcrypt
from datetime import datetime, timedelta
from jose import jwt

from app.crud import crud_user
from app.schema.auth import UserToken
from app.settings import (
    ACCESS_TOKEN_EXPIRE,
    REFRESH_TOKEN_EXPIRE,
    JWT_SECRET,
    ALGORITHM,
)
from app.cache.jwt_handle import add_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def validate_login(db: Session, email: str, password: str) -> Any:
    user = crud_user.user.get_by_email(db=db, email=email)

    if not user:
        raise HTTPException(status_code=400, detail="Email not found!!!!")

    hashed_password = user.hashed_password.encode("utf-8")
    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        raise HTTPException(status_code=400, detail="Wrong password!!!!")

    return user


def create_user_token(email, keep_login=False) -> UserToken:
    access_token = _create_token(
        token_type="access_token",
        lifetime=timedelta(seconds=ACCESS_TOKEN_EXPIRE),
        sub=email,
    )
    refresh_token = (
        _create_token(
            token_type="access_token",
            lifetime=timedelta(seconds=REFRESH_TOKEN_EXPIRE),
            sub=email,
        )
        if keep_login
        else ""
    )

    add_jwt(access_token, email, expire=ACCESS_TOKEN_EXPIRE)
    add_jwt(refresh_token, email, expire=REFRESH_TOKEN_EXPIRE)

    return UserToken(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
):
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
