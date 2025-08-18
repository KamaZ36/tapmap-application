from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.user_role import UserRole
   

@dataclass(frozen=True)
class CurrentUser:
    user_id: UUID
    roles: list[UserRole]
