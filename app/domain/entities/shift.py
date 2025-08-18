from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from app.domain.entities.base import Entity


class ShiftStatus(str, Enum):
    active = "active"
    

@dataclass(kw_only=True)
class Shift(Entity):
    driver_id: UUID
