from typing import Any

from fastapi import status
from fastapi.exceptions import HTTPException

from config.config import NotFoundError
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    def __init__(
        self,
        repository: PostRepository,
        user_repository: UserRepository,
    ) -> None:
        self._repository = repository
        self._user_repository = user_repository

    async def list_posts(self) -> list[Post]:
        return await self._repository.list_all()

    async def get_post(self, post_id: int) -> Post:
        post = await self._repository.get_by_id(post_id)
        if post is None:
            raise NotFoundError('Post', post_id)
        return post

    async def list_posts_for_user(self, user_id: int) -> list[Post]:
        if not await self._user_repository.exists(user_id):
            raise NotFoundError('User', user_id)
        return await self._repository.list_by_user_id(user_id)

    async def create_post(self, data: PostCreate) -> Any | None:
        if not await self._user_repository.exists(data.user_id):
            raise NotFoundError('User', data.user_id)

        return await self._repository.create(
            title=data.title,
            content=data.content,
            user_id=data.user_id,
        )

    async def update_post(self, post_id: int, data: PostUpdate) -> Post:
        post = await self._repository.get_by_id(post_id)

        if post is None:
            raise NotFoundError('Post', post_id)

        if post.user_id != data.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You are not allowed to update this post',
            )

        return await self._repository.update(post, data)

    async def update_post_partial(self, post_id: int, data: PostUpdate) -> Post:
        post = await self._repository.get_by_id(post_id)

        if post is None:
            raise NotFoundError('Post', post_id)

        return await self._repository.update_partial(post, data)

    async def delete_post(self, post_id: int) -> None:
        post = await self._repository.get_by_id(post_id)

        if post is None:
            raise NotFoundError('Post', post_id)

        await self._repository.delete(post)
