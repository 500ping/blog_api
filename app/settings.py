import os

DEBUG = int(os.getenv('DEBUG', 1))

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
if DEBUG:
    SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"

JWT_SECRET = 'secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE: int = (60 * 60 * 3)  # 3 hours
# 60 seconds * 60 minutes * 24 hours * 3 days = 3 days
REFRESH_TOKEN_EXPIRE: int = (60 * 60 * 24 * 3)
