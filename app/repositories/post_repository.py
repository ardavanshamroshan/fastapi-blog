from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.post import Post
from app.schemas.post import PostUpdate


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
            raise RuntimeError(f'Failed to load post {post.id} after create')
        return loaded

    def update(self, post: Post, data: PostUpdate) -> Post:
        post.title = data.title
        post.content = data.content

        self._db.commit()
        self._db.refresh(post)

        return post

    def update_partial(self, post: Post, data: PostUpdate) -> Post:
        """Update a post partially. for fields that were not provided in the request, the field will not be updated."""

        # Convert the Pydantic model to a dict, excluding fields that were not provided in the request
        data = data.model_dump(exclude_unset=True)

        # Iterates over each field and its corresponding value from the provided data,
        # and updates the respective attributes of the post object dynamically.
        for field, value in data.items():
            setattr(post, field, value)

        self._db.commit()
        self._db.refresh(post)

        return post

    def delete(self, post: Post):
        self._db.delete(post)
        self._db.commit()
        
        return post