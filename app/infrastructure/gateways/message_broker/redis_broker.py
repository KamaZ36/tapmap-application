import json

from typing import Any
from redis.asyncio import Redis
from loguru import logger

from app.infrastructure.gateways.message_broker.base import BaseMessageBrokerGateway


class RedisMessageBrokerGateway(BaseMessageBrokerGateway):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def start(self) -> None:
        logger.info("Redis Pub/Sub готов к работе.")

    async def stop(self) -> None: ...

    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        value_bytes = json.dumps(value).encode()
        await self.redis.publish(channel=topic, message=value_bytes)
