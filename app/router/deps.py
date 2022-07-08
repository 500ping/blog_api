from this import d
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError

from app.db.session import SessionLocal
from app.security.authentication import oauth2_scheme
from app.model import User
from app import settings
from app.crud import crud_user
from app.redis.jwt_handle import check_jwt


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not check_jwt(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This token has been expried or not exist!!!"
            )
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud_user.user.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user
