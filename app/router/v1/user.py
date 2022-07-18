from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Any

from app.schema.user import UserCreate, User
from app.router import deps
from app.crud import crud_user
from app.model import User as UserModel

user_router = APIRouter(prefix="/user")


@user_router.get("/me", response_model=User)
async def my_profile(current_user: UserModel = Depends(deps.get_current_user)) -> User:
    return current_user


@user_router.get("/me/update", response_model=User)
async def update_profile(
    current_user: UserModel = Depends(deps.get_current_user),
) -> User:
    return {"message": "Todo later"}


@user_router.get("/me/change-password", response_model=User)
async def change_password(
    current_user: UserModel = Depends(deps.get_current_user),
) -> User:
    return {"message": "Todo later"}
