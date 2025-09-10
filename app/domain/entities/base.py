from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID
from app.domain.utils.uuid_v7 import uuid7
from datetime import datetime

from app.infrastructure.database.models.base import get_datetime_utc_now


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid7)
    created_at: datetime = field(default_factory=get_datetime_utc_now)
    updated_at: datetime = field(default_factory=get_datetime_utc_now)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
