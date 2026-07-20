import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Comment, Post
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.db.redis import get_cache, set_cache, delete_pattern
from app.core.config import settings


async def create_comment(db: AsyncSession, comment_data: dict) -> Comment:
    comment = Comment(**comment_data)
    
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    post_id = comment.post_id
    await delete_pattern(f"post:{post_id}:comments:*")
    await delete_pattern(f"post:{post_id}:comments_count")

    return comment


async def get_comments_by_post_id(db: AsyncSession, post_id: uuid.UUID, limit: int = 10) -> list[Comment]:
    cache_key = f"post:{post_id}:comments:last{limit}"
    
    cached = await get_cache(cache_key)
    if cached:
        return cached

    query = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    comments = result.scalars().all()
    comments_list = list(comments)
    
    await set_cache(cache_key, comments_list, settings.CACHE_TTL_COMMENTS)
    
    return comments_list


async def get_comment_by_id(comment_id: uuid.UUID, db: AsyncSession) -> Comment | None:

    query = (
        select(Comment)
        .where(Comment.id == comment_id))
    
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def delete_comment(comment: Comment, db: AsyncSession) -> None:
    post_id = comment.post_id
    await db.delete(comment)
    await db.commit()
    
    await delete_pattern(f"post:{post_id}:comments:*")
    await delete_pattern(f"post:{post_id}:comments_count")
