import redis

from .conn import redis_session


def add_jwt(token, username, expire=None):
    redis_session.set(token, username, ex=expire)


def delete_jwt(token):
    redis_session.delete(token)


def check_jwt(token):
    return redis_session.get(token)
