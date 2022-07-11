from fastapi import APIRouter, Depends
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
from app.cache.jwt_handle import delete_jwt


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


@auth_router.post('/refresh', response_model=UserToken)
async def get_refresh_token(
    *,
    db: Session = Depends(deps.get_db),
    request: RefreshRequest
) -> Any:
    refresh_token = request.refresh_token
    user = deps.get_current_user(db, token=refresh_token)
    delete_jwt(refresh_token)
    return authentication.create_user_token(user.email, keep_login=True)
