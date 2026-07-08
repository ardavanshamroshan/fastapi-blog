from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    """Base model for a post. without default values means they are required."""
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=1000)
    author: str = Field(min_length=1, max_length=50)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    """Response model for a post. ConfigDict is used to convert the model to a dictionary. from_attributes=True means that the model will be converted to a dictionary using the attributes of the model."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_created: str
    date_updated: str
