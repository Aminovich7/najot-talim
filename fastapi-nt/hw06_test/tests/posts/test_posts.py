"""Integration tests for blog post endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from tests.factories import create_author, create_post


@pytest.mark.asyncio
async def test_list_posts_empty(client: AsyncClient) -> None:
    response = await client.get("/posts")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_post_as_author(
    client: AsyncClient,
    author_user: User,
    author_auth_headers: dict[str, str],
) -> None:
    response = await client.post(
        "/posts",
        headers=author_auth_headers,
        json={"title": "My First Post", "content": "Hello from the author."},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Post"
    assert data["content"] == "Hello from the author."
    assert data["author_id"] == author_user.id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_post_unauthorized(client: AsyncClient) -> None:
    response = await client.post(
        "/posts",
        json={"title": "Nope", "content": "No token provided."},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_post_forbidden_for_regular_user(
    client: AsyncClient,
    user_auth_headers: dict[str, str],
) -> None:
    response = await client.post(
        "/posts",
        headers=user_auth_headers,
        json={"title": "Nope", "content": "Readers cannot write."},
    )
    assert response.status_code == 403
    assert "Author privileges" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_validation_error(
    client: AsyncClient,
    author_auth_headers: dict[str, str],
) -> None:
    response = await client.post(
        "/posts",
        headers=author_auth_headers,
        json={"title": "", "content": "Missing title"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_post_by_id(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
) -> None:
    post = await create_post(db_session, author_user, title="Readable")
    await db_session.commit()

    response = await client.get(f"/posts/{post.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Readable"


@pytest.mark.asyncio
async def test_get_post_not_found(client: AsyncClient) -> None:
    response = await client.get("/posts/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_list_posts_returns_created(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
) -> None:
    await create_post(db_session, author_user, title="One")
    await create_post(db_session, author_user, title="Two")
    await db_session.commit()

    response = await client.get("/posts")
    assert response.status_code == 200
    titles = {item["title"] for item in response.json()}
    assert titles == {"One", "Two"}


@pytest.mark.asyncio
async def test_update_own_post(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
    author_auth_headers: dict[str, str],
) -> None:
    post = await create_post(db_session, author_user, title="Old", content="Old body")
    await db_session.commit()

    response = await client.put(
        f"/posts/{post.id}",
        headers=author_auth_headers,
        json={"title": "New", "content": "New body"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New"
    assert data["content"] == "New body"


@pytest.mark.asyncio
async def test_update_own_post_partial(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
    author_auth_headers: dict[str, str],
) -> None:
    post = await create_post(db_session, author_user, title="Keep", content="Change me")
    await db_session.commit()

    response = await client.put(
        f"/posts/{post.id}",
        headers=author_auth_headers,
        json={"content": "Changed"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Keep"
    assert data["content"] == "Changed"


@pytest.mark.asyncio
async def test_update_post_empty_payload(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
    author_auth_headers: dict[str, str],
) -> None:
    post = await create_post(db_session, author_user)
    await db_session.commit()

    response = await client.put(
        f"/posts/{post.id}",
        headers=author_auth_headers,
        json={},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_other_authors_post_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
    author_auth_headers: dict[str, str],
) -> None:
    other = await create_author(
        db_session,
        username="other_author",
        email="other@example.com",
    )
    post = await create_post(db_session, other, title="Not yours")
    await db_session.commit()

    response = await client.put(
        f"/posts/{post.id}",
        headers=author_auth_headers,
        json={"title": "Hijack"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_post_not_found(
    client: AsyncClient,
    author_auth_headers: dict[str, str],
) -> None:
    response = await client.put(
        "/posts/99999",
        headers=author_auth_headers,
        json={"title": "Ghost"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_post_unauthorized(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
) -> None:
    post = await create_post(db_session, author_user)
    await db_session.commit()

    response = await client.put(
        f"/posts/{post.id}",
        json={"title": "No auth"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_own_post(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
    author_auth_headers: dict[str, str],
) -> None:
    post = await create_post(db_session, author_user, title="Delete me")
    await db_session.commit()

    response = await client.delete(
        f"/posts/{post.id}",
        headers=author_auth_headers,
    )
    assert response.status_code == 204

    follow_up = await client.get(f"/posts/{post.id}")
    assert follow_up.status_code == 404


@pytest.mark.asyncio
async def test_delete_other_authors_post_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
    author_auth_headers: dict[str, str],
) -> None:
    other = await create_author(
        db_session,
        username="rival",
        email="rival@example.com",
    )
    post = await create_post(db_session, other)
    await db_session.commit()

    response = await client.delete(
        f"/posts/{post.id}",
        headers=author_auth_headers,
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_post_unauthorized(
    client: AsyncClient,
    db_session: AsyncSession,
    author_user: User,
) -> None:
    post = await create_post(db_session, author_user)
    await db_session.commit()

    response = await client.delete(f"/posts/{post.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_post_not_found(
    client: AsyncClient,
    author_auth_headers: dict[str, str],
) -> None:
    response = await client.delete("/posts/99999", headers=author_auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_database_integrity_author_required(
    client: AsyncClient,
    author_auth_headers: dict[str, str],
    author_user: User,
) -> None:
    """Creating a post ties it to the authenticated author (FK integrity)."""
    response = await client.post(
        "/posts",
        headers=author_auth_headers,
        json={"title": "Owned", "content": "By the token subject"},
    )
    assert response.status_code == 201
    assert response.json()["author_id"] == author_user.id


# ---------------------------------------------------------------------------
# Unit tests (commented out — uncomment to run in isolation)
# ---------------------------------------------------------------------------
#
# import pytest
# from unittest.mock import AsyncMock, MagicMock, patch
#
# from fastapi import HTTPException
# from app.posts.schemas import PostCreate, PostUpdate
# from app.posts import service as post_service
# from app.users.models import UserRole
#
#
# @pytest.mark.asyncio
# async def test_get_post_raises_404_unit() -> None:
#     db = AsyncMock()
#     with patch("app.posts.service.post_crud.get_post_by_id", new=AsyncMock(return_value=None)):
#         with pytest.raises(HTTPException) as exc_info:
#             await post_service.get_post(db, 1)
#         assert exc_info.value.status_code == 404
#
#
# @pytest.mark.asyncio
# async def test_update_own_post_forbidden_unit() -> None:
#     db = AsyncMock()
#     author = MagicMock(id=1, role=UserRole.AUTHOR)
#     foreign_post = MagicMock(id=10, author_id=2)
#     payload = PostUpdate(title="X")
#     with patch("app.posts.service.get_post", new=AsyncMock(return_value=foreign_post)):
#         with pytest.raises(HTTPException) as exc_info:
#             await post_service.update_own_post(db, 10, payload, author)
#         assert exc_info.value.status_code == 403
#
#
# @pytest.mark.asyncio
# async def test_delete_own_post_forbidden_unit() -> None:
#     db = AsyncMock()
#     author = MagicMock(id=1, role=UserRole.AUTHOR)
#     foreign_post = MagicMock(id=10, author_id=2)
#     with patch("app.posts.service.get_post", new=AsyncMock(return_value=foreign_post)):
#         with pytest.raises(HTTPException) as exc_info:
#             await post_service.delete_own_post(db, 10, author)
#         assert exc_info.value.status_code == 403
#
#
# @pytest.mark.asyncio
# async def test_create_post_for_author_unit() -> None:
#     db = AsyncMock()
#     author = MagicMock(id=5)
#     payload = PostCreate(title="T", content="C")
#     created = MagicMock(id=1, title="T", content="C", author_id=5)
#     with patch("app.posts.service.post_crud.create_post", new=AsyncMock(return_value=created)) as mock_create:
#         result = await post_service.create_post_for_author(db, payload, author)
#         assert result is created
#         mock_create.assert_awaited_once()
