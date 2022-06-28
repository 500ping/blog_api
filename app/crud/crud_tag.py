from typing import Optional
from sqlalchemy.orm import Session

from app.model.tag import Tag
from app.schema.tag import (
    TagCreate,
    TagUpdate,
)
from app.crud.base import CRUDBase


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Tag]:
        return db.query(Tag).filter(Tag.name == name).first()

tag = CRUDTag(Tag)
