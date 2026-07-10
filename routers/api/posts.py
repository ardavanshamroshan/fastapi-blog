from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.providers.services import get_post_service
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.services.post_service import PostService

router = APIRouter(prefix='/api/posts', tags=['posts'])


@router.get(path='/', response_model=list[PostResponse], name='api.posts.index')
def index(
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return post_service.list_posts()


@router.get(path='/{post_id}', response_model=PostResponse, name='api.posts.show')
def show(
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return post_service.get_post(post_id)


@router.post(
    path='/',
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    name='api.posts.store',
)
def store(
    post: PostCreate,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return post_service.create_post(post)


@router.put(
    path='/{post_id}',
    response_model=PostResponse,
    name='api.posts.update'
)
def update(
    post_id: int,
    post: PostUpdate,
    post_service: Annotated[PostService, Depends(get_post_service)]
):
    return post_service.update_post(post_id, post)


@router.patch(
    path='/partial/{post_id}',
    response_model=PostResponse,
    name='api.posts.update.partial'
)
def update_partial(
    post_id: int,
    post: PostUpdate,
    post_service: Annotated[PostService, Depends(get_post_service)]
):
    return post_service.update_post_partial(post_id, post)

@router.delete(
    path='/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    name='api.posts.delete'
)
def delete(
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)]
):
    return post_service.delete_post(post_id)
