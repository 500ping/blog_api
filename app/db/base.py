# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.model.user import User
from app.model.post import Post
from app.model.tag import Tag
from app.model.post_tags import PostTag
