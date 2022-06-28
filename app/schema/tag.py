from typing import Optional
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    ...


class TagUpdate(TagBase):
    ...


class TagInDBBase(TagBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Tag(TagInDBBase):
    ...
