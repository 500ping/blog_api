from app.db.base_class import Base
from app.model.post_tags import PostTag
from app.model.tag import Tag

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    ForeignKey,
    Text,
    Boolean,
    event,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, Session
from sqlalchemy import func
from slugify import slugify


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    overview = Column(String, index=True)
    content = Column(Text)
    time_read = Column(Integer)
    view_count = Column(Integer)
    slug = Column(String, unique=True)
    is_publish = Column(Boolean)

    created_on = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="posts")

    tags = relationship("Tag", secondary=PostTag.__table__, back_populates="posts")
    tag_ids = association_proxy("tags", "id")

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


event.listen(Post.title, "set", Post.generate_slug, retval=False)
