"""Database operations for posts."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.models import Post


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    """Fetch a post by primary key."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def list_posts(
    db: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[Post]:
    """Return a paginated list of posts ordered by creation date descending."""
    result = await db.execute(
        select(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def create_post(
    db: AsyncSession,
    *,
    title: str,
    content: str,
    author_id: int,
) -> Post:
    """Persist a new post and return it."""
    post = Post(title=title, content=content, author_id=author_id)
    db.add(post)
    await db.flush()
    await db.refresh(post)
    return post


async def update_post(
    db: AsyncSession,
    post: Post,
    *,
    title: str | None = None,
    content: str | None = None,
) -> Post:
    """Apply partial updates to an existing post."""
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    await db.flush()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post: Post) -> None:
    """Delete a post from the database."""
    await db.delete(post)
    await db.flush()
