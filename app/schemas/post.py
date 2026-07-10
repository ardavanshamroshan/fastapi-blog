from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserResponse


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=1000)


class PostCreate(PostBase):
    user_id: int

class PostUpdate(PostBase):
    title: str | None = Field(default=None,min_length=1, max_length=100)
    content: str | None = Field(default=None,min_length=1, max_length=1000)
    user_id: int | None = Field(default=None)

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_created: datetime
    date_updated: datetime
    author: UserResponse
