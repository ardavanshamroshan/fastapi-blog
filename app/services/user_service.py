from config.config import ConflictError, NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def get_user(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError('User', user_id)
        return user

    async def create_user(self, data: UserCreate) -> User:
        existing_user = await self._repository.get_by_username_or_email(
            username=data.username,
            email=data.email,
        )
        if existing_user:
            raise ConflictError('Username or email already exists')

        return await self._repository.create(
            username=data.username,
            email=data.email,
        )

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        """Update a user"""

        user = await self.find_or_raise(user_id)
        await self.check_username_availability(user.username, data.username)
        await self.check_email_availability(user.email, data.email)

        return await self._repository.update(user, data)

    async def update_user_partial(self, user_id: int, data: UserUpdate) -> User:
        """Update a user partially"""

        user = await self.find_or_raise(user_id)
        await self.check_username_availability(user.username, data.username)
        await self.check_email_availability(user.email, data.email)

        return await self._repository.update_partial(user, data)

    async def find_or_raise(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError('User', user_id)
        return user

    async def check_username_availability(
        self, current_username: str, username: str
    ) -> bool:
        """Check if the username is available"""

        existing_user = await self._repository.get_by_username_or_email(
            username=username,
            email=None,
        )

        return existing_user is None

    async def check_email_availability(
        self, current_email: str | None, email: str
    ) -> bool:
        """Check if the email is available"""

        existing_user = await self._repository.get_by_username_or_email(
            username=None,
            email=email,
        )

        return existing_user is None

    async def delete_user(self, user_id: int) -> None:
        """Delete a user"""

        user = await self.find_or_raise(user_id)
        await self._repository.delete(user)
