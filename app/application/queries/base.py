from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


class Query(ABC): ...


QT = TypeVar("QT", bound=Query)
QR = TypeVar("QR", bound=Any)


class QueryHandler(ABC, Generic[QT, QR]):
    @abstractmethod
    async def __call__(self, query: QT) -> QR: ...
