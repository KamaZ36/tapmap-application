from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


class BaseCommand(ABC): ...


CT = TypeVar("CT", bound=BaseCommand)
CR = TypeVar("CR", bound=Any)


class CommandHandler(ABC, Generic[CT, CR]):
    @abstractmethod
    async def __call__(self, command: CT) -> CR: ...
