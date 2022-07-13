from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder

from app.model.post import Post
from app.model.tag import Tag
from app.schema.post import (
    PostCreate,
    PostUpdate,
)
from app.crud.base import CRUDBase
from app.crud import crud_post_tags


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_multi(
            self,
            db: Session,
            *,
            skip: int = 0,
            limit: int = 100,
            filter = None,
            search = None
    ) -> List[Post]:
        qs = db.query(Post)
        if filter:
            qs = qs.join(Post.tags).filter(Tag.name == filter)
        if search:
            search = f"%{search}%"
            qs = qs.filter(or_(Post.title.ilike(search),
                               Post.overview.ilike(search)))
        qs = qs.offset(skip).limit(limit)
        return qs.all()

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Post]:
        return db.query(Post).filter(Post.slug == slug).first()

    def get_by_title(self, db: Session, *, title: str) -> Optional[Post]:
        return db.query(Post).filter(Post.title == title).first()

    def _handle_tags(self, db, post_id, tag_ids, is_create=True):
        if not is_create:
            crud_post_tags.post_tag.delete_post_tags(db, post_id=post_id)
        for tag_id in tag_ids:
            crud_post_tags.post_tag.create(db, post_id, tag_id)

    def create(
            self,
            db: Session,
            *,
            obj_in: PostCreate,
            created_by,
    ) -> Post:
        obj_in_data = jsonable_encoder(obj_in)
        tag_ids = obj_in_data.pop('tag_ids', [])  # Get tag_ids

        db_obj = self.model(**obj_in_data, created_by=created_by)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        self._handle_tags(db, db_obj.id, tag_ids)

        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: Post,
            obj_in: PostUpdate
    ) -> Post:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

            tag_ids = update_data.pop('tag_ids', False)  # Get tag_ids
            if tag_ids:
                self._handle_tags(db, db_obj.id, tag_ids, is_create=False)

        for field, value in obj_data.items():
            if field in update_data and value != update_data[field]:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


post = CRUDPost(Post)
