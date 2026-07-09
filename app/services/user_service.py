from config.config import ConflictError, NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def get_user(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user

    def create_user(self, data: UserCreate) -> User:
        existing_user = self._repository.get_by_username_or_email(
            username=data.username,
            email=data.email,
        )
        if existing_user:
            raise ConflictError("Username or email already exists")

        return self._repository.create(
            username=data.username,
            email=data.email,
        )
