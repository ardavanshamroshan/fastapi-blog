from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self._db.scalar(select(User).where(User.id == user_id))

    def get_by_username_or_email(self, *, username: str, email: str) -> User | None:
        return self._db.scalar(
            select(User).where(
                or_(User.username == username, User.email == email)
            )
        )

    def exists(self, user_id: int) -> bool:
        return (
            self._db.scalar(select(User.id).where(
                User.id == user_id)) is not None
        )

    def create(self, *, username: str, email: str) -> User:
        user = User(username=username, email=email)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update(self, user: User, data: UserUpdate) -> User:
        user.username = data.username
        user.email = data.email
        user.image_file = data.image_file

        self._db.commit()
        self._db.refresh(user)

        return user

    def update_partial(self, user: User, data: UserUpdate) -> User:
        """Update a user partially"""
        data = data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(user, field, value)

        self._db.commit()
        self._db.refresh(user)

        return user

    def delete(self, user: User) -> None:
        self._db.delete(user)
        self._db.commit()

        return user
