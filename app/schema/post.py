from pydantic import BaseModel
from typing import Optional, Sequence


class PostRequest(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str


class PostsResponse(BaseModel):
    results: Sequence[PostResponse]
