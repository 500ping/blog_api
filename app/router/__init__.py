from fastapi import APIRouter

from .post import post_router
from .user import user_router

router = APIRouter()
router.include_router(post_router)
router.include_router(user_router)
