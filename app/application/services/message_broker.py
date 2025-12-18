from typing import Any
from app.infrastructure.gateways.message_broker.base import BaseMessageBrokerGateway


class MessageBrokerService:
    def __init__(self, broker_gateway: BaseMessageBrokerGateway) -> None:
        self.broker_gateway = broker_gateway

    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        await self.broker_gateway.publish(topic=topic, key=key, value=value)
