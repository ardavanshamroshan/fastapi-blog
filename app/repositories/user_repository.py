from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User


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
            self._db.scalar(select(User.id).where(User.id == user_id)) is not None
        )

    def create(self, *, username: str, email: str) -> User:
        user = User(username=username, email=email)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
