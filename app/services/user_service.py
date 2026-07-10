from config.config import ConflictError, NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def get_user(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError('User', user_id)
        return user

    def create_user(self, data: UserCreate) -> User:
        existing_user = self._repository.get_by_username_or_email(
            username=data.username,
            email=data.email,
        )
        if existing_user:
            raise ConflictError('Username or email already exists')

        return self._repository.create(
            username=data.username,
            email=data.email,
        )

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        """Update a user"""

        user = self._repository.get_by_id(user_id)

        self.findOrRaise(user_id)
        self.check_username_availability(user.username, data.username)
        self.check_email_availability(user.email, data.email)

        return self._repository.update(user, data)

    def update_user_partial(self, user_id: int, data: UserUpdate) -> User:
        """Update a user partially"""

        user = self._repository.get_by_id(user_id)

        self.findOrRaise(user_id)
        self.check_username_availability(user.username, data.username)
        self.check_email_availability(user.email, data.email)

        return self._repository.update_partial(user, data)

    def findOrRaise(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError('User', user_id)
        return user

    def check_username_availability(self, current_username: str, username: str) -> bool:
        """Check if the username is available"""

        existing_user = self._repository.get_by_username_or_email(
            username=username,
            email=None,
        )

        return existing_user is None

    def check_email_availability(self, current_email: str | None, email: str) -> bool:
        """Check if the email is available"""

        existing_user = self._repository.get_by_username_or_email(
            username=None,
            email=email,
        )

        return existing_user is None

    def delete_user(self, user_id: int) -> None:
        """Delete a user"""

        user = self._repository.get_by_id(user_id)

        self.findOrRaise(user_id)

        return self._repository.delete(user)
