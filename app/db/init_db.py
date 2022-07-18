import logging
from sqlalchemy.orm import Session
from getpass import getpass

from app.crud import crud_user
from app.schema.user import UserCreate


def create_user(db: Session) -> None:
    print("Creating user...")
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    password = getpass("Enter password: ")
    re_password = getpass("Re-enter password: ")

    user = crud_user.user.get_by_email(db=db, email=email)
    if user:
        print("User with this email already exist")
        return

    if password != re_password:
        print("Password does not match")
        return

    user_in = UserCreate(full_name=full_name, email=email, password=password)

    user = crud_user.user.create(db=db, obj_in=user_in)
    print("User created!!!")
