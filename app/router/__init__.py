from fastapi import APIRouter

from .post import post_router
from .user import user_router
from .tag import tag_router
from .auth import auth_router

router = APIRouter()
router.include_router(post_router)
router.include_router(user_router)
router.include_router(tag_router)
router.include_router(auth_router)
