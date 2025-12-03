from functools import lru_cache
from redis.asyncio import Redis

from app.core.config import settings


@lru_cache()
def get_redis_client() -> Redis:
    return Redis.from_url(settings.redis_url)
