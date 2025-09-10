from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass(frozen=True)
class ValueObject(ABC):
    pass
