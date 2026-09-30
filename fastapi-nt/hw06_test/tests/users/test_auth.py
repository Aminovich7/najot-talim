"""Integration tests for authentication and user profile endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password
from app.users import crud as user_crud
from app.users.models import User, UserRole


@pytest.mark.asyncio
async def test_register_regular_user(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123",
            "role": "user",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "hashed_password" not in data
    assert "id" in data


@pytest.mark.asyncio
async def test_register_author(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "password123",
            "role": "author",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "author"


@pytest.mark.asyncio
async def test_register_duplicate_username(
    client: AsyncClient,
    regular_user: User,
) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "username": regular_user.username,
            "email": "other@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_duplicate_email(
    client: AsyncClient,
    regular_user: User,
) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "username": "otheruser",
            "email": regular_user.email,
            "password": "password123",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_validation_error_short_password(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "short",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_validation_error_invalid_email(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "not-an-email",
            "password": "password123",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, regular_user: User) -> None:
    response = await client.post(
        "/auth/login",
        json={"username": regular_user.username, "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, regular_user: User) -> None:
    response = await client.post(
        "/auth/login",
        json={"username": regular_user.username, "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_user(client: AsyncClient) -> None:
    response = await client.post(
        "/auth/login",
        json={"username": "nobody", "password": "password123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, db_session: AsyncSession) -> None:
    user = await user_crud.create_user(
        db_session,
        username="inactive",
        email="inactive@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.USER,
    )
    user.is_active = False
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"username": "inactive", "password": "password123"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_jwt_authentication_users_me(
    client: AsyncClient,
    regular_user: User,
    user_auth_headers: dict[str, str],
) -> None:
    response = await client.get("/users/me", headers=user_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == regular_user.id
    assert data["username"] == regular_user.username


@pytest.mark.asyncio
async def test_users_me_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_users_me_invalid_token(client: AsyncClient) -> None:
    response = await client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_users_me_inactive_token(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    user = await user_crud.create_user(
        db_session,
        username="gone",
        email="gone@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.USER,
    )
    await db_session.commit()
    token = create_access_token(subject=user.id)
    user.is_active = False
    await db_session.commit()

    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Unit tests (commented out — uncomment to run in isolation)
# ---------------------------------------------------------------------------
#
# import pytest
# from unittest.mock import AsyncMock, MagicMock, patch
#
# from fastapi import HTTPException
# from app.users.schemas import UserCreate, UserLogin
# from app.users.models import UserRole
# from app.users import service as user_service
# from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
#
#
# def test_hash_and_verify_password_unit() -> None:
#     hashed = hash_password("secretpass")
#     assert hashed != "secretpass"
#     assert verify_password("secretpass", hashed) is True
#     assert verify_password("wrong", hashed) is False
#
#
# def test_create_and_decode_access_token_unit() -> None:
#     token = create_access_token(subject=42, extra_claims={"role": "author"})
#     payload = decode_access_token(token)
#     assert payload["sub"] == "42"
#     assert payload["role"] == "author"
#
#
# @pytest.mark.asyncio
# async def test_register_user_raises_on_duplicate_unit() -> None:
#     db = AsyncMock()
#     payload = UserCreate(
#         username="alice",
#         email="alice@example.com",
#         password="password123",
#         role=UserRole.USER,
#     )
#     with patch("app.users.service.user_crud.get_user_by_username_or_email", new=AsyncMock(return_value=MagicMock())):
#         with pytest.raises(HTTPException) as exc_info:
#             await user_service.register_user(db, payload)
#         assert exc_info.value.status_code == 400
#
#
# @pytest.mark.asyncio
# async def test_authenticate_user_invalid_credentials_unit() -> None:
#     db = AsyncMock()
#     payload = UserLogin(username="alice", password="bad")
#     with patch("app.users.service.user_crud.get_user_by_username", new=AsyncMock(return_value=None)):
#         with pytest.raises(HTTPException) as exc_info:
#             await user_service.authenticate_user(db, payload)
#         assert exc_info.value.status_code == 401
