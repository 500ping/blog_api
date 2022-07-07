from typing import Optional
from sqlalchemy.orm import Session
import bcrypt

from app.crud.base import CRUDBase
from app.model.user import User
from app.schema.user import (
    UserCreate,
    UserUpdate,
)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed_password = bcrypt.hashpw(
            obj_in.password.encode('utf-8'), bcrypt.gensalt())

        user = User(
            full_name=obj_in.full_name,
            email=obj_in.email,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user = CRUDUser(User)
