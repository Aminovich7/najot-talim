import json
import redis.asyncio as redis
from app.core.config import settings

redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def get_cache(key: str) -> dict | list | None:
    client = await get_redis()
    value = await client.get(key)
    if value:
        return json.loads(value)
    return None


async def set_cache(key: str, value: dict | list, ttl: int):
    client = await get_redis()
    await client.set(key, json.dumps(value), ex=ttl)


async def delete_cache(key: str):
    client = await get_redis()
    await client.delete(key)


async def delete_pattern(pattern: str):
    client = await get_redis()
    keys = await client.keys(pattern)
    if keys:
        await client.delete(*keys)
