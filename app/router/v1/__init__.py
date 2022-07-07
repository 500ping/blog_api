from fastapi import APIRouter

from .post import post_router
from .user import user_router
from .tag import tag_router
from .auth import auth_router

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(post_router)
v1_router.include_router(user_router)
v1_router.include_router(tag_router)
v1_router.include_router(auth_router)
