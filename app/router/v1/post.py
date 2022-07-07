from typing import Any, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schema.post import (
    PostCreate,
    PostUpdate,
    Post
)
from app.router import deps
from app.crud import (
    crud_post,
)
from app.model import User as UserModel

post_router = APIRouter(prefix="/post")


@post_router.get('/', status_code=200, response_model=List[Post])
async def get_posts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:

    posts = crud_post.post.get_multi(db, skip=skip, limit=limit)

    return posts


# @post_router.get('/{post_id}', status_code=200, response_model=Post)
# async def get_post(
#     *,
#     db: Session = Depends(deps.get_db),
#     post_id: int
# ) -> Any:

#     post = crud_post.post.get(db, id=post_id)
#     if not post:
#         raise HTTPException(
#             status_code=400,
#             detail=f"The post with id {post_id} does not exists in the system.",
#         )

#     return post


@post_router.get('/{slug}', status_code=200, response_model=Post)
async def get_post_by_slug(
    *,
    db: Session = Depends(deps.get_db),
    slug: str
) -> Any:

    post = crud_post.post.get_by_slug(db, slug=slug)
    if not post:
        raise HTTPException(
            status_code=400,
            detail=f"Post not found!!!",
        )

    return post


@post_router.post('/', status_code=201, response_model=Post)
async def create_post(
    *,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
    post_in: PostCreate,
) -> Any:

    post = crud_post.post.get_by_title(db, title=post_in.title)
    if post:
        raise HTTPException(
            status_code=400,
            detail="The post with this title already exists in the system.",
        )

    post = crud_post.post.create(
        db, obj_in=post_in, created_by=current_user.id)
    return post


@post_router.put('/{post_id}', status_code=200, response_model=Post)
async def update_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id,
    post_in: PostUpdate,
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:

    post = crud_post.post.get(db, post_id)

    if not post:
        raise HTTPException(
            status_code=400,
            detail=f"The post with id {post_id} does not exists in the system.",
        )

    post = crud_post.post.update(db, db_obj=post, obj_in=post_in)
    return post


@post_router.delete('/{post_id}', status_code=200, response_model=Post)
async def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id,
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:

    post = crud_post.post.get(db, post_id)
    if not post:
        raise HTTPException(
            status_code=400,
            detail=f"The post with id {post_id} does not exists in the system.",
        )

    post = crud_post.post.remove(db, id=post_id)
    return post
