from config.config import NotFoundError
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.post import PostCreate


class PostService:
    def __init__(
        self,
        repository: PostRepository,
        user_repository: UserRepository,
    ) -> None:
        self._repository = repository
        self._user_repository = user_repository

    def list_posts(self) -> list[Post]:
        return self._repository.list_all()

    def get_post(self, post_id: int) -> Post:
        post = self._repository.get_by_id(post_id)
        if post is None:
            raise NotFoundError("Post", post_id)
        return post

    def list_posts_for_user(self, user_id: int) -> list[Post]:
        if not self._user_repository.exists(user_id):
            raise NotFoundError("User", user_id)
        return self._repository.list_by_user_id(user_id)

    def create_post(self, data: PostCreate) -> Post:
        if not self._user_repository.exists(data.user_id):
            raise NotFoundError("User", data.user_id)

        return self._repository.create(
            title=data.title,
            content=data.content,
            user_id=data.user_id,
        )
