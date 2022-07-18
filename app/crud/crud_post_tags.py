from sqlalchemy.orm import Session

from app.model.post_tags import PostTag


class CRUDPostTag:
    def create(self, db: Session, post_id, tag_id):
        post_tag = PostTag(post_id=post_id, tag_id=tag_id)
        db.add(post_tag)
        db.commit()
        db.refresh(post_tag)
        return post_tag

    def delete_post_tags(
        self,
        db: Session,
        post_id,
    ):
        delete_q = PostTag.__table__.delete().where(PostTag.post_id == post_id)
        db.execute(delete_q)
        db.commit()
        return


post_tag = CRUDPostTag()
