import logging
from sqlalchemy.orm import Session
from getpass import getpass

from app.crud import crud_user
from app.schema.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_user(db: Session) -> None:
    logger.info('Creating user...')
    full_name = input('Enter full name: ')
    email = input('Enter email: ')
    password = getpass('Enter password: ')
    re_password = getpass('Re-enter password: ')

    user = crud_user.user.get_by_email(db=db, email=email)
    if user:
        logger.error('The user with this email already exists in the system!')
        return

    if password != re_password:
        logger.error('Password does not match!')
        return

    user_in = UserCreate(
        full_name=full_name,
        email=email,
        password=password
    )

    user = crud_user.user.create(db=db, obj_in=user_in)
    logger.info('User is created...')