from datetime import datetime

from pydantic import BaseModel, Field

try:
    from pydantic import ConfigDict
except ImportError:  # Pydantic v1 fallback
    ConfigDict = None


class ORMBaseModel(BaseModel):
    if ConfigDict is not None:
        model_config = ConfigDict(from_attributes=True)
    else:  # Pydantic v1 fallback
        class Config:
            orm_mode = True


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    image: str | None = Field(default=None, max_length=120)
    desc: str | None = None
    author_id: int
    category_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    image: str | None = Field(default=None, max_length=120)
    desc: str | None = None
    author_id: int | None = None
    category_id: int | None = None


class BookRead(ORMBaseModel):
    id: int
    title: str
    image: str | None = None
    desc: str | None = None
    author_id: int
    category_id: int
    created_at: datetime | None = None


class CommentBase(BaseModel):
    sumary: str = Field(..., min_length=1, max_length=128)
    user: str = Field(..., min_length=1, max_length=12)
    book_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    sumary: str | None = Field(default=None, min_length=1, max_length=128)
    user: str | None = Field(default=None, min_length=1, max_length=12)
    book_id: int | None = None


class CommentRead(ORMBaseModel):
    id: int
    sumary: str
    user: str
    book_id: int


class SavedBase(BaseModel):
    user: str = Field(..., min_length=1, max_length=12)
    book_id: int


class SavedCreate(SavedBase):
    pass


class SavedUpdate(BaseModel):
    user: str | None = Field(default=None, min_length=1, max_length=12)
    book_id: int | None = None


class SavedRead(ORMBaseModel):
    id: int
    user: str
    book_id: int
