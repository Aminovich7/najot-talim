"""HTTP routes for blog posts."""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.posts.dependencies import get_post_or_404
from app.posts.models import Post
from app.posts.schemas import PostCreate, PostRead, PostUpdate
from app.posts.service import (
    create_post_for_author,
    delete_own_post,
    get_posts,
    update_own_post,
)
from app.users.dependencies import get_current_author
from app.users.models import User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostRead])
async def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> list[Post]:
    """List published posts (public)."""
    return await get_posts(db, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostRead)
async def read_post(post: Post = Depends(get_post_or_404)) -> Post:
    """Retrieve a single post by id (public)."""
    return post


@router.post(
    "",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    payload: PostCreate,
    db: AsyncSession = Depends(get_db),
    author: User = Depends(get_current_author),
) -> Post:
    """Create a new post (authors only)."""
    return await create_post_for_author(db, payload, author)


@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    payload: PostUpdate,
    db: AsyncSession = Depends(get_db),
    author: User = Depends(get_current_author),
) -> Post:
    """Update own post (authors only)."""
    return await update_own_post(db, post_id, payload, author)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    author: User = Depends(get_current_author),
) -> Response:
    """Delete own post (authors only)."""
    await delete_own_post(db, post_id, author)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
