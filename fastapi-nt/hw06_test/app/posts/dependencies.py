"""FastAPI dependencies for the posts feature."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.posts.models import Post
from app.posts.service import get_post


async def get_post_or_404(
    post_id: int,
    db: AsyncSession = Depends(get_db),
) -> Post:
    """Resolve a post by path parameter or raise 404."""
    return await get_post(db, post_id)
