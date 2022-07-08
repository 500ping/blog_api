from fastapi import FastAPI
import uvicorn
import sys
import logging

from app.router import router
from app.db import session, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = "localhost"
PORT = 8069

app = FastAPI()
app.include_router(router)

def create_user() -> None:
    db = session.SessionLocal()
    init_db.create_user(db=db)


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "run":
        uvicorn.run("main:app", host=HOST, port=PORT, reload=True, log_level="info")
    elif args[0] == 'createuser':
        create_user()
    else:
        logger.warning('Only accept run or createuser.')
