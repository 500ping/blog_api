from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Any

from app.schema.user import (
    UserCreate,
    User
)
from app.router import deps
from app.crud import (
    crud_user
)

user_router = APIRouter(prefix="/user")


@user_router.post('/', status_code=201, response_model=User)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:

    user = crud_user.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = crud_user.user.create(db, obj_in=user_in)

    return user
