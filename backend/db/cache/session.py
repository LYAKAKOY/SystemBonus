from redis import asyncio as aioredis
import settings


async def get_redis():
    session = await aioredis.from_url(settings.REDIS_URL, db=1)
    try:
        yield session
    finally:
        await session.aclose()
