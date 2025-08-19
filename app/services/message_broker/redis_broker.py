import json
from dataclasses import dataclass
from typing import Any
from redis.asyncio import Redis
from loguru import logger


@dataclass
class RedisMessageBroker:
    redis: Redis
    
    async def start(self) -> None:
        logger.info("Redis Pub/Sub готов к работе.")
        
    async def stop(self) -> None:
        ...  
    
    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        value_bytes = json.dumps(value).encode()
        await self.redis.publish(channel=topic, message=value_bytes)
