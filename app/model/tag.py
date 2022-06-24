from app.db.base_class import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Tag(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    posts = relationship('Post', secondary='post_tags', back_populates='tags')
