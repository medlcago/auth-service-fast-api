from typing import Optional

from redis import asyncio as aioredis

from storage import Store, _ExpireType


class RedisStore(Store):
    def __init__(self, url: str):
        self.redis = aioredis.from_url(url)

    async def set(self, key: str, value: str, expire: _ExpireType = None):
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> Optional[str]:
        value = await self.redis.get(key)
        return value.decode("utf-8") if value else None

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) > 0
