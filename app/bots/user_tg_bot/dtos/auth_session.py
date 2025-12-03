from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.utils.uuid_v7 import uuid7
from app.utils.get_datetime_utc_now import get_datetime_utc_now


@dataclass(kw_only=True)
class AuthSession:
    id: UUID = field(default_factory=uuid7)
    tg_id: int
    user_id: UUID
    created_at: datetime = field(default_factory=get_datetime_utc_now)
