from fastapi import APIRouter, HTTPException

from ..schema.post import (
    PostRequest,
    PostResponse,
    PostsResponse
)

post_router = APIRouter()

POST = [
    {
        "id": 1,
        "title": "title 1",
        "content": "content 1"
    },
    {
        "id": 2,
        "title": "title 2",
        "content": "content 2"
    },
    {
        "id": 3,
        "title": "title 3",
        "content": "content 3"
    },
    {
        "id": 4,
        "title": "title 4",
        "content": "content 4"
    },
]


@post_router.get('/post', status_code=200, response_model=PostsResponse)
def get_posts():
    return {
        "results": POST
    }


@post_router.get('/post/{id}', status_code=200, response_model=PostResponse)
def get_post(id: int):
    post = list(filter(lambda post: post.get('id') == id, POST))

    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post {id} not found"
        )

    return post[0]


@post_router.post('/post', status_code=201, response_model=PostResponse)
def create_post(request: PostRequest):
    post = {
        'id': POST[-1].get('id') + 1 if len(POST) else 1,
        **request.dict()
    }
    POST.append(post)

    return post


@post_router.put('/post/{id}', status_code=201, response_model=PostResponse)
def update_post(id: int, request: PostRequest):
    post = list(filter(lambda post: post.get('id') == id, POST))

    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post {id} not found"
        )

    post[0]["title"] = request.title
    post[0]["content"] = request.content
    print(POST)

    return post[0]


@post_router.delete('/post/{id}', status_code=200)
def update_post(id: int):
    for i, post in enumerate(POST):
        if post['id'] == id:
            return POST.pop(i)

    raise HTTPException(
            status_code=404, detail=f"Post {id} not found"
        )
