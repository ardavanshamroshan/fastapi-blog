from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._db.scalar(select(User).where(User.id == user_id))

    async def get_by_username_or_email(
        self, *, username: str | None, email: str | None
    ) -> User | None:
        return await self._db.scalar(
            select(User).where(
                or_(User.username == username, User.email == email)
            )
        )

    async def exists(self, user_id: int) -> bool:
        return (
            await self._db.scalar(select(User.id).where(User.id == user_id))
            is not None
        )

    async def create(self, *, username: str, email: str) -> User:
        user = User(username=username, email=email)
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def update(self, user: User, data: UserUpdate) -> User:
        user.username = data.username
        user.email = data.email
        user.image_file = data.image_file

        await self._db.commit()
        await self._db.refresh(user)

        return user

    async def update_partial(self, user: User, data: UserUpdate) -> User:
        """Update a user partially"""
        data = data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(user, field, value)

        await self._db.commit()
        await self._db.refresh(user)

        return user

    async def delete(self, user: User) -> User:
        await self._db.delete(user)
        await self._db.commit()

        return user
