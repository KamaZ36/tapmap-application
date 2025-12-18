from abc import ABC, abstractmethod
from typing import Any


class BaseMessageBrokerGateway(ABC):
    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        raise NotImplementedError()
