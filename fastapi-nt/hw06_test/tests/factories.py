"""Test data factories for users and posts."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.posts import crud as post_crud
from app.posts.models import Post
from app.users import crud as user_crud
from app.users.models import User, UserRole


async def create_regular_user(
    db: AsyncSession,
    *,
    username: str = "reader",
    email: str = "reader@example.com",
    password: str = "password123",
) -> User:
    """Create and return a regular user."""
    return await user_crud.create_user(
        db,
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.USER,
    )


async def create_author(
    db: AsyncSession,
    *,
    username: str = "writer",
    email: str = "writer@example.com",
    password: str = "password123",
) -> User:
    """Create and return an author user."""
    return await user_crud.create_user(
        db,
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.AUTHOR,
    )


async def create_post(
    db: AsyncSession,
    author: User,
    *,
    title: str = "Hello World",
    content: str = "This is a sample post.",
) -> Post:
    """Create and return a post owned by the given author."""
    return await post_crud.create_post(
        db,
        title=title,
        content=content,
        author_id=author.id,
    )
