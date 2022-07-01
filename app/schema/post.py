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
    created_by: int
    tag_ids: List[int]
    # tags: List[int]


class PostUpdate(PostBase):
    tag_ids: List[int]


class PostInDBBase(PostBase):
    id: Optional[int] = None
    owner: User
    tags: List[Tag]

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    ...
