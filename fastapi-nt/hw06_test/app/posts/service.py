"""Business logic for blog posts."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts import crud as post_crud
from app.posts.models import Post
from app.posts.schemas import PostCreate, PostUpdate
from app.users.models import User


async def get_posts(
    db: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[Post]:
    """Return a paginated list of posts."""
    return await post_crud.list_posts(db, skip=skip, limit=limit)


async def get_post(db: AsyncSession, post_id: int) -> Post:
    """Return a post or raise 404."""
    post = await post_crud.get_post_by_id(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


async def create_post_for_author(
    db: AsyncSession,
    payload: PostCreate,
    author: User,
) -> Post:
    """Create a new post owned by the given author."""
    return await post_crud.create_post(
        db,
        title=payload.title,
        content=payload.content,
        author_id=author.id,
    )


async def update_own_post(
    db: AsyncSession,
    post_id: int,
    payload: PostUpdate,
    author: User,
) -> Post:
    """Update a post if it belongs to the author."""
    post = await get_post(db, post_id)
    if post.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to modify this post",
        )
    if payload.title is None and payload.content is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update",
        )
    return await post_crud.update_post(
        db,
        post,
        title=payload.title,
        content=payload.content,
    )


async def delete_own_post(
    db: AsyncSession,
    post_id: int,
    author: User,
) -> None:
    """Delete a post if it belongs to the author."""
    post = await get_post(db, post_id)
    if post.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this post",
        )
    await post_crud.delete_post(db, post)
