from typing import Optional, List
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

    def get_tags_by_ids(self, db: Session, *, tag_ids: List[str]) -> List[Tag]:
        return db.query(Tag).filter(Tag.id.in_(tag_ids))


tag = CRUDTag(Tag)
