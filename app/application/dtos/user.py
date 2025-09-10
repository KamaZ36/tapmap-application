from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.user_role import UserRole


@dataclass(frozen=True)
class CurrentUser:
    user_id: UUID
    roles: list[UserRole]


@dataclass(frozen=True)
class GetUsersFilters:
    phone_number: str | None = None
    completed_orders_max: int | None = None
    completed_orders_min: int | None = None
    cancelled_orders_max: int | None = None
    cancelled_orders_min: int | None = None
    limit: int | None = 5
    offset: int | None = 0
