import redis

from app.settings import REDIS_URL

redis_session = redis.from_url(REDIS_URL)
