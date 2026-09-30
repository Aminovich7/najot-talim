"""Shared pytest fixtures for async API tests."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.users.models import User
from tests.factories import create_author, create_regular_user

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_engine():
    """Create an in-memory async SQLite engine for a single test."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session bound to the test engine."""
    session_factory = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with session_factory() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTPX async client with the app database dependency overridden."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session
        await db_session.commit()

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
    app.dependency_overrides.clear()


@pytest.fixture
async def regular_user(db_session: AsyncSession) -> User:
    """Persist a regular (non-author) user."""
    user = await create_regular_user(db_session)
    await db_session.commit()
    return user


@pytest.fixture
async def author_user(db_session: AsyncSession) -> User:
    """Persist an author user."""
    user = await create_author(db_session)
    await db_session.commit()
    return user


@pytest.fixture
def user_token(regular_user: User) -> str:
    """JWT access token for the regular user fixture."""
    return create_access_token(
        subject=regular_user.id,
        extra_claims={"role": regular_user.role.value},
    )


@pytest.fixture
def author_token(author_user: User) -> str:
    """JWT access token for the author fixture."""
    return create_access_token(
        subject=author_user.id,
        extra_claims={"role": author_user.role.value},
    )


@pytest.fixture
def user_auth_headers(user_token: str) -> dict[str, str]:
    """Authorization headers for a regular user."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def author_auth_headers(author_token: str) -> dict[str, str]:
    """Authorization headers for an author."""
    return {"Authorization": f"Bearer {author_token}"}
