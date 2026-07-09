from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.providers.services import get_post_service
from app.schemas.post import PostCreate, PostResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=list[PostResponse], name="api.posts.index")
def index(
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return post_service.list_posts()


@router.get("/{post_id}", response_model=PostResponse, name="api.posts.show")
def show(
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return post_service.get_post(post_id)


@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    name="api.posts.store",
)
def store(
    post: PostCreate,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return post_service.create_post(post)
