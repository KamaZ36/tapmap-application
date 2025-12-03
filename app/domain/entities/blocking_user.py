from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.base import Entity
from app.utils import get_datetime_utc_now


@dataclass(kw_only=True)
class BlockingUser(Entity):
    user_id: UUID
    reason: str
    is_active: bool = True
    expires_at: datetime

    def is_expired(self) -> bool:
        """Проверка, истекла ли блокировка

        Returns:
            bool: True - блокировка истекла, False - блокировка активна (не истекла)
        """
        datetime_now = get_datetime_utc_now()
        return datetime_now > self.expires_at

    def unblock(self) -> None:
        self.is_active = False
