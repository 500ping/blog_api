from fastapi import APIRouter

from .post import post_router

router = APIRouter()
router.include_router(post_router)
