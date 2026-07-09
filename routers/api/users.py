from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.providers.services import get_post_service, get_user_service
from app.schemas.post import PostResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.post_service import PostService
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    path="/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    name="api.users.store",
)
def store(
    user: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse, name="api.users.show")
def show(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.get_user(user_id)


@router.get(
    "/{user_id}/posts",
    response_model=list[PostResponse],
    name="api.users.posts",
)
def posts(
    user_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return post_service.list_posts_for_user(user_id)
