from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import settings

SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI
connect_args = {}

if settings.DEBUG:
    connect_args['check_same_thread'] = False

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
