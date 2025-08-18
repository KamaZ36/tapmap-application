import json
from typing import Any
from app.services.message_broker.base import BaseMessageBroker
from aiokafka import AIOKafkaProducer


class KafkaMessageBroker(BaseMessageBroker): 
    
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer
    
    async def start(self) -> None:
        await self._producer.start()
        
    async def stop(self) -> None:
        await self._producer.stop()
    
    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        value_bytes = json.dumps(value).encode()
        key_bytes = key.encode()
        await self._producer.send(
            topic=topic,
            key=key_bytes,
            value=value_bytes
        )
    