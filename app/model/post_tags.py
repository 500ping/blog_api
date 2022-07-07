from app.db.base_class import Base

from sqlalchemy import Column, ForeignKey, Integer


class PostTag(Base):
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'))
    tag_id = Column(Integer, ForeignKey('tag.id', ondelete='CASCADE'))
