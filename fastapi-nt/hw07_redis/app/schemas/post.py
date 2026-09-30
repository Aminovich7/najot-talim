from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.comment import CommentOut

class PostCreate(BaseModel):
    title : str = Field(min_length=5, max_length=255)
    content : str = Field(min_length=1, max_length=10000)


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=255)
    content: str | None = Field(default=None, min_length=1, max_length=10000)


class PostOut(BaseModel):
    id: UUID
    author_id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int 
    model_config = {"from_attributes": True}

class PostDetail(BaseModel):
    id: UUID
    author_id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int 
    comments: list[CommentOut]
    model_config = {"from_attributes": True}