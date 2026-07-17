"""Business logic for authentication and users."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.users import crud as user_crud
from app.users.models import User
from app.users.schemas import Token, UserCreate, UserLogin


async def register_user(db: AsyncSession, payload: UserCreate) -> User:
    """Register a new user or raise if credentials already exist."""
    existing = await user_crud.get_user_by_username_or_email(
        db,
        username=payload.username,
        email=payload.email,
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    return await user_crud.create_user(
        db,
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )


async def authenticate_user(db: AsyncSession, payload: UserLogin) -> Token:
    """Validate credentials and return a JWT access token."""
    user = await user_crud.get_user_by_username(db, payload.username)
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    token = create_access_token(subject=user.id, extra_claims={"role": user.role.value})
    return Token(access_token=token)
