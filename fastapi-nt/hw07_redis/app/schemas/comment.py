from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import UUID


class CommentCreate(BaseModel):
    content : str = Field(min_length=1, max_length=2000)


class CommentOut(BaseModel):
    id: UUID
    post_id: UUID
    author_id: UUID
    content: str
    created_at: datetime
    author_username: str 