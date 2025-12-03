from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.user import User, UserBlocking
from app.domain.enums.user import UserRole, UserStatus


@dataclass(frozen=True)
class CurrentUser:
    user_id: UUID
    roles: list[UserRole]


@dataclass(frozen=True, eq=False)
class UserBlockingDTO:
    id: UUID
    reason: str
    expires_at: datetime
    created_at: datetime

    @classmethod
    def from_entity(cls, user_blocking: UserBlocking) -> "UserBlockingDTO":
        return cls(
            id=user_blocking.id,
            reason=user_blocking.reason,
            expires_at=user_blocking.expires_at,
            created_at=user_blocking.created_at,
        )


@dataclass(frozen=True, eq=False, kw_only=True)
class UserDTO:
    id: UUID
    name: str
    phone_number: str
    status: UserStatus
    completed_orders_count: int
    cancelled_orders_count: int
    base_city_id: UUID | None = None
    roles: list[UserRole]
    created_at: datetime
    blocking: UserBlockingDTO | None = None

    @classmethod
    def from_entity(cls, user: User, blocking: UserBlocking | None = None) -> "UserDTO":
        user_blocking_dto = None
        if blocking:
            user_blocking_dto = UserBlockingDTO.from_entity(blocking)

        return UserDTO(
            id=user.id,
            name=user.name,
            phone_number=user.phone_number.value,
            status=user.status,
            completed_orders_count=user.completed_orders_count,
            cancelled_orders_count=user.cancelled_orders_count,
            base_city_id=user.base_city_id,
            roles=user.roles,
            created_at=user.created_at,
            blocking=user_blocking_dto,
        )


@dataclass(frozen=True)
class GetUsersFilters:
    phone_number: str | None = None
    completed_orders_max: int | None = None
    completed_orders_min: int | None = None
    cancelled_orders_max: int | None = None
    cancelled_orders_min: int | None = None
    limit: int | None = 5
    offset: int | None = 0


@dataclass(frozen=True, eq=False)
class UserForOrderDTO:
    id: UUID
    name: str
    phone_number: str
