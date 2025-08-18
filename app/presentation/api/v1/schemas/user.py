from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.domain.entities.user import User, UserRole


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
    
class ResponseUserSchema(BaseModel):
    id: UUID
    name: str
    phone_number: str
    completed_orders_count: int
    cancelled_orders_count: int
    roles: list[str]
    base_city_id: UUID | None = None
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> 'ResponseUserSchema':
        return cls(
            id=user.id, 
            name=user.name,
            phone_number=user.phone_number.value,
            completed_orders_count=user.completed_orders_count,
            cancelled_orders_count=user.cancelled_orders_count,
            roles=[role.value for role in user.roles],
            base_city_id=user.base_city_id,
            created_at=user.created_at
        )
