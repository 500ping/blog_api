JWT_SECRET = 'secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE: int = (60 * 3)  # 3 hours
# 60 minutes * 24 hours * 3 days = 3 days
REFRESH_TOKEN_EXPIRE: int = (60 * 24 * 3)
