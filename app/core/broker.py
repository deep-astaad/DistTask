import json
from redis.asyncio import Redis

from app.core.config import settings


class RedisBroker:
    def __init__(self):
        self.redis = Redis.from_url(settings.redis_url)

    async def publish(self, queue: str, message: dict):
        await self.redis.rpush(queue, json.dumps(message))

    async def consume(self, queue: str):
        _, data = await self.redis.blpop(queue)

        return json.loads(data)

    async def close(self):
        await self.redis.close()


broker = RedisBroker()