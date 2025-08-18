from typing import Any, Protocol


class BaseMessageBroker(Protocol):
    
    async def start(self) -> None: ...
    
    async def stop(self) -> None: ...
    
    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None: ...
