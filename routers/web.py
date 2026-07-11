from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.providers.services import get_post_service, get_user_service
from app.services.post_service import PostService
from app.services.user_service import UserService
from config.config import templates

router = APIRouter(include_in_schema=False)


@router.get('/', name='home.index')
async def home(
    request: Request,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context={'posts': await post_service.list_posts()},
    )


@router.get('/posts', name='posts.index')
async def index(
    request: Request,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    return templates.TemplateResponse(
        request=request,
        name='posts/index.html',
        context={'posts': await post_service.list_posts()},
    )


@router.get('/posts/{post_id}', name='posts.show')
async def show(
    request: Request,
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    post = await post_service.get_post(post_id)
    return templates.TemplateResponse(
        request=request,
        name='posts/show.html',
        context={'post': post, 'title': post.title},
    )


@router.get('/users/{user_id}/posts', name='users.posts.index')
async def user_posts(
    request: Request,
    user_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    author = await user_service.get_user(user_id)
    posts = await post_service.list_posts_for_user(user_id)

    return templates.TemplateResponse(
        request=request,
        name='posts/index.html',
        context={
            'posts': posts,
            'author': author,
        },
    )
