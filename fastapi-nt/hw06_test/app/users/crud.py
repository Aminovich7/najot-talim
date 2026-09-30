"""Database operations for users."""

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User, UserRole


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Fetch a user by primary key."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Fetch a user by username."""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetch a user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username_or_email(
    db: AsyncSession,
    username: str,
    email: str,
) -> User | None:
    """Fetch a user matching either username or email."""
    result = await db.execute(
        select(User).where(or_(User.username == username, User.email == email))
    )
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    *,
    username: str,
    email: str,
    hashed_password: str,
    role: UserRole,
) -> User:
    """Persist a new user and return it."""
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user
