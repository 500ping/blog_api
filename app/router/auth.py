from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.router import deps
from app.security import authentication
from app.schema.auth import (
    UserToken,
    RefreshRequest,
    UserLogin
)
from app.schema.user import User
from app.model.user import User as UserModel


auth_router = APIRouter(prefix='/auth')


@auth_router.post('/login', response_model=UserToken)
async def login(
    *,
    db: Session = Depends(deps.get_db),
    login_form: UserLogin,
    ) -> Any:
    email = login_form.email
    password = login_form.password
    keep_login = login_form.keep_login

    user = authentication.validate_login(db, email, password)
    return authentication.create_user_token(user.email, keep_login)

@auth_router.get('/me', response_model=User)
async def my_profile(
    current_user: UserModel = Depends(deps.get_current_user)
) -> User:
    return current_user

@auth_router.post('/refresh', response_model=UserToken)
async def get_refresh_token(
    *,
    db: Session = Depends(deps.get_db),
    request: RefreshRequest
) -> Any:
    user = deps.get_current_user(db, token=request.refresh_token)
    return authentication.create_user_token(user.email)
