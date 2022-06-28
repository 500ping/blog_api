from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.model.post import Post
from app.schema.post import (
    PostCreate,
    PostUpdate,
)
from app.crud.base import CRUDBase
from app.crud import crud_tag


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Post]:
        return db.query(Post).filter(Post.slug == slug).first()

    def get_by_title(self, db: Session, *, title: str) -> Optional[Post]:
        return db.query(Post).filter(Post.title == title).first()

    def create(
        self, db: Session, *, obj_in: PostCreate, created_by
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_by=created_by)

        tags = crud_tag.tag.get_tags_by_ids(db, tag_ids=db_obj.tags)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

post = CRUDPost(Post)
