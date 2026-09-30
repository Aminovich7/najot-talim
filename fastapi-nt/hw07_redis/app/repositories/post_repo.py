import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Post
from sqlalchemy.orm import selectinload
from datetime import datetime
from sqlalchemy import select, func, or_
from app.db.redis import get_cache, set_cache, delete_pattern
from app.core.config import settings

async def create_post(post_data:dict, db : AsyncSession) -> Post:
    post = Post(**post_data)
    
    db.add(post)
    await db.commit()
    await db.refresh(post)

    await delete_pattern("posts:*")

    return post

async def get_post_by_id(post_id: uuid.UUID, db: AsyncSession) -> Post | None:

    query = (
        select(Post)
        .where(Post.id == post_id)
        .options(selectinload(Post.likes))
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_post_detail_by_id(post_id: uuid.UUID, db: AsyncSession) -> Post | None:
    cache_key = f"post:{post_id}:detail"
    
    cached = await get_cache(cache_key)
    if cached:
        return cached

    query = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.comments),
            selectinload(Post.likes),
        )
    )
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    
    if post:
        await set_cache(cache_key, post, settings.CACHE_TTL_POSTS)
    
    return post


async def get_posts(
    db: AsyncSession, page: int = 1, page_size: int = 10, search: str | None = None, 
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> tuple[list[Post], int]:
    cache_key = f"posts:page:{page}:size:{page_size}:search:{search or ''}:from:{date_from or ''}:to:{date_to or ''}"
    
    cached = await get_cache(cache_key)
    if cached:
        return cached['posts'], cached['total']

    query = select(Post).options(selectinload(Post.likes))
    count_query = select(func.count()).select_from(Post)

    if search:
        search_filter = or_(
            Post.title.ilike(f"%{search}%"),
            Post.content.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    if date_from:
        query = query.where(Post.created_at >= date_from)
        count_query = count_query.where(Post.created_at >= date_from)

    if date_to:
        query = query.where(Post.created_at <= date_to)
        count_query = count_query.where(Post.created_at <= date_to)

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    query = (
        query.order_by(Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(query)
    posts = result.scalars().all()

    posts_list = list(posts)
    await set_cache(cache_key, {'posts': posts_list, 'total': total}, settings.CACHE_TTL_POSTS)

    return posts_list, total


async def update_post(db, post: Post, update_data: dict) -> Post:
    for key, value in update_data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    
    await delete_pattern(f"post:{post.id}:*")
    await delete_pattern("posts:*")
    
    return post

    
async def delete_post(db, post: Post) -> None:
    post_id = post.id
    await db.delete(post)
    await db.commit()
    
    await delete_pattern(f"post:{post_id}:*")
    await delete_pattern("posts:*")

async def get_posts_older_than(db: AsyncSession, cutoff_datetime: datetime) -> list[Post]:
    query = select(Post).where(Post.created_at <= cutoff_datetime)
    
    result = await db.execute(query)
    posts = result.scalars().all()

    return list(posts)