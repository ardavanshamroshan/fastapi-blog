from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.providers.database import get_db
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.post_service import PostService
from app.services.user_service import UserService

DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


def get_post_repository(db: DbSession) -> PostRepository:
    return PostRepository(db)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)


def get_post_service(
    post_repository: Annotated[PostRepository, Depends(get_post_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> PostService:
    return PostService(post_repository, user_repository)
