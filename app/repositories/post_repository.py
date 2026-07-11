from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.post import Post
from app.schemas.post import PostUpdate


class PostRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    def _base_query(self):
        return select(Post).options(selectinload(Post.author))

    async def list_all(self) -> list[Post]:
        result = await self._db.scalars(
            self._base_query().order_by(Post.date_created.desc())
        )
        return list(result.all())

    async def get_by_id(self, post_id: int) -> Post | None:
        return await self._db.scalar(self._base_query().where(Post.id == post_id))

    async def list_by_user_id(self, user_id: int) -> list[Post]:
        result = await self._db.scalars(
            self._base_query()
            .where(Post.user_id == user_id)
            .order_by(Post.date_created.desc())
        )
        return list(result.all())

    async def create(self, *, title: str, content: str, user_id: int) -> Any | None:
        post = Post(title=title, content=content, user_id=user_id)
        self._db.add(post)
        await self._db.commit()
        await self._db.refresh(post, attribute_names=['author'])
        loaded = await self._db.scalar(self._base_query().where(Post.id == post.id))
        if loaded is None:
            raise RuntimeError(f'Failed to load post {post.id} after create')
        return loaded

    async def update(self, post: Post, data: PostUpdate) -> Post:
        post.title = data.title
        post.content = data.content

        await self._db.commit()
        await self._db.refresh(post)

        return post

    async def update_partial(self, post: Post, data: PostUpdate) -> Post:
        """Update a post partially. for fields that were not provided in the request, the field will not be updated."""

        data = data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(post, field, value)

        await self._db.commit()
        await self._db.refresh(post)

        return post

    async def delete(self, post: Post) -> Post:
        await self._db.delete(post)
        await self._db.commit()

        return post
