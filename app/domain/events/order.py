from dataclasses import dataclass
from uuid import UUID

from app.domain.events.base import Event


@dataclass(frozen=True, eq=False)
class OrderConfirmed(Event):
    order_id: UUID
