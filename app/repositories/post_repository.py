from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _base_query(self):
        return select(Post).options(joinedload(Post.author))

    def list_all(self) -> list[Post]:
        return list(
            self._db.scalars(
                self._base_query().order_by(Post.date_created.desc())
            ).all()
        )

    def get_by_id(self, post_id: int) -> Post | None:
        return self._db.scalar(self._base_query().where(Post.id == post_id))

    def list_by_user_id(self, user_id: int) -> list[Post]:
        return list(
            self._db.scalars(
                self._base_query()
                .where(Post.user_id == user_id)
                .order_by(Post.date_created.desc())
            ).all()
        )

    def create(self, *, title: str, content: str, user_id: int) -> Post:
        post = Post(title=title, content=content, user_id=user_id)
        self._db.add(post)
        self._db.commit()
        self._db.refresh(post)
        loaded = self._db.scalar(self._base_query().where(Post.id == post.id))
        if loaded is None:
            raise RuntimeError(f"Failed to load post {post.id} after create")
        return loaded
