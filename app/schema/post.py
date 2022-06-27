from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Sequence


class PostBase(BaseModel):
    title: str
    overview: str
    content: str
    time_read: int
    view_count: int
    is_publish: bool


class PostRequest(PostBase):
    ...


class PostResponse(PostBase):
    id: int
    title: str
    content: str


class PostsResponse(BaseModel):
    results: Sequence[PostResponse]
