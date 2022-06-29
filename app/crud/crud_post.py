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
from app.crud import crud_post_tags


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Post]:
        return db.query(Post).filter(Post.slug == slug).first()

    def get_by_title(self, db: Session, *, title: str) -> Optional[Post]:
        return db.query(Post).filter(Post.title == title).first()

    def create(
        self, 
        db: Session, 
        *, 
        obj_in: PostCreate, 
        # created_by,
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        tag_ids = obj_in_data.pop('tag_ids', []) # Get tag_ids

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Handle tags
        for tag_id in tag_ids:
            crud_post_tags.post_tag.create(db, db_obj.id, tag_id)

        return db_obj

post = CRUDPost(Post)
