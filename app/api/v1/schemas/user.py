from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.application.dtos.user import UserBlockingDTO, UserDTO, UserForOrderDTO
from app.domain.entities.user import User, UserRole


class GetUsersFiltersSchema(BaseModel):
    phone_number: str | None = None
    completed_orders_max: int | None = None
    completed_orders_min: int | None = None
    cancelled_orders_max: int | None = None
    cancelled_orders_min: int | None = None
    limit: int | None = 5
    offset: int | None = 0


class CurrentUserSchema(BaseModel):
    user_id: UUID
    roles: list[UserRole]


class CreateUserSchema(BaseModel):
    name: str
    phone_number: str


class UpdateUserBaseLocationSchema(BaseModel):
    coordinates: tuple[float, float]


class ResponseUserForOrder(BaseModel):
    id: UUID
    name: str
    phone_number: str


class ResponseBlockingSchema(BaseModel):
    id: UUID
    reason: str
    expires_at: datetime
    created_at: datetime

    @classmethod
    def from_dto(cls, user_blocking_dto: UserBlockingDTO) -> "ResponseBlockingSchema":
        return ResponseBlockingSchema(
            id=user_blocking_dto.id,
            reason=user_blocking_dto.reason,
            expires_at=user_blocking_dto.expires_at,
            created_at=user_blocking_dto.created_at,
        )


class ResponseUserSchema(BaseModel):
    id: UUID
    name: str
    phone_number: str
    completed_orders_count: int
    cancelled_orders_count: int
    roles: list[UserRole]
    base_city_id: UUID | None = None
    created_at: datetime
    blocking: ResponseBlockingSchema | None = None

    @classmethod
    def from_dto(cls, user: UserDTO) -> "ResponseUserSchema":
        blocking_schema = None
        if user.blocking:
            blocking_schema = ResponseBlockingSchema.from_dto(user.blocking)

        return cls(
            id=user.id,
            name=user.name,
            phone_number=user.phone_number,
            completed_orders_count=user.completed_orders_count,
            cancelled_orders_count=user.cancelled_orders_count,
            roles=user.roles,
            base_city_id=user.base_city_id,
            created_at=user.created_at,
            blocking=blocking_schema,
        )


class ResponseCustomerForOrderSchema(BaseModel):
    id: UUID
    name: str
    phone_number: str

    @classmethod
    def from_dto(cls, user: UserForOrderDTO) -> "ResponseCustomerForOrderSchema":
        return ResponseCustomerForOrderSchema(
            id=user.id, name=user.name, phone_number=user.phone_number
        )
