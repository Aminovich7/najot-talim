import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Comment, Post, Like
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from app.db.redis import get_cache, set_cache, delete_pattern
from app.core.config import settings


async def create_like(user_id: uuid.UUID, post_id: uuid.UUID, db: AsyncSession) -> Like:
    like = Like(user_id=user_id, post_id=post_id)

    db.add(like)
    await db.commit()
    await db.refresh(like)

    await delete_pattern(f"post:{post_id}:likes_count")

    return like


async def get_like(user_id: uuid.UUID, post_id: uuid.UUID, db: AsyncSession) -> Like | None:
    query = select(Like).where(
        Like.user_id == user_id,
        Like.post_id == post_id,
    )

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def delete_like(db: AsyncSession, like: Like) -> None:
    post_id = like.post_id
    await db.delete(like)
    await db.commit()
    
    await delete_pattern(f"post:{post_id}:likes_count")


async def count_likes_for_post(db: AsyncSession, post_id: uuid.UUID) -> int:
    cache_key = f"post:{post_id}:likes_count"
    
    cached = await get_cache(cache_key)
    if cached is not None:
        return cached

    query = select(func.count()).select_from(Like).where(Like.post_id == post_id)

    result = await db.execute(query)
    count = result.scalar_one()
    
    await set_cache(cache_key, count, settings.CACHE_TTL_COUNTS)
    
    return count  


async def get_like_user_ids_for_post(db: AsyncSession, post_id: uuid.UUID) -> list[uuid.UUID]:
    """
    Berilgan postga layk bosgan barcha foydalanuvchilarning
    user_id larini ro'yxat qilib qaytaradi.
    /feed endPointidagi "likes": ["<uuid1>", "<uuid2>"] formatiga
    mos kelish uchun ishlatiladi.
    """
    query = select(Like.user_id).where(Like.post_id == post_id)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_comments_for_post(db: AsyncSession, post_id: uuid.UUID) -> int:
    cache_key = f"post:{post_id}:comments_count"
    
    cached = await get_cache(cache_key)
    if cached is not None:
        return cached

    query = select(func.count()).select_from(Comment).where(Comment.post_id == post_id)

    result = await db.execute(query)
    count = result.scalar_one()
    
    await set_cache(cache_key, count, settings.CACHE_TTL_COUNTS)
    
    return count