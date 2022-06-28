from typing import Any, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..schema.post import (
    PostCreate,
    PostUpdate,
    Post
)
from app.router import deps
from app.crud import crud_post, crud_user

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


@post_router.get('/{post_id}', status_code=200, response_model=Post)
async def get_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int
    ) -> Any:

    post = crud_post.post.get(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=400,
            detail=f"The post with id {post_id} does not exists in the system.",
        )

    return post


@post_router.post('/', status_code=201, response_model=Post)
async def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: PostCreate,
    ) -> Any:

    post = crud_post.post.get_by_title(db, title=post_in.title)
    if post:
        raise HTTPException(
            status_code=400,
            detail="The post with this title already exists in the system.",
        )

    user = crud_user.user.get(db, id=1)
    post = crud_post.post.create(db, obj_in=post_in, created_by=user.id)
    return post


# @post_router.put('/post/{id}', status_code=201, response_model=PostResponse)
# async def update_post(id: int, request: PostRequest):
#     post = list(filter(lambda post: post.get('id') == id, POST))

#     if not post:
#         raise HTTPException(
#             status_code=404, detail=f"Post {id} not found"
#         )

#     post[0]["title"] = request.title
#     post[0]["content"] = request.content
#     print(POST)

#     return post[0]


# @post_router.delete('/post/{id}', status_code=200)
# async def update_post(id: int):
#     for i, post in enumerate(POST):
#         if post['id'] == id:
#             return POST.pop(i)

#     raise HTTPException(
#             status_code=404, detail=f"Post {id} not found"
#         )
