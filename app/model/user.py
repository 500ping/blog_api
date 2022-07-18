from app.db.base_class import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="owner")
