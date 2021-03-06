from pydantic import BaseModel
from typing import List, Optional

from .tag import Tag
from .user import User


class PostBase(BaseModel):
    title: str
    overview: str
    content: str
    time_read: int
    view_count: int
    is_publish: bool


class PostCreate(PostBase):
    tag_ids: List[int]


class PostUpdate(PostBase):
    tag_ids: List[int]


class PostInDBBase(PostBase):
    id: Optional[int] = None
    slug: str
    owner: User
    tags: List[Tag]

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    ...
