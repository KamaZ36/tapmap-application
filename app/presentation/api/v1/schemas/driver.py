from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.domain.entities.driver import Driver, DriverStatus


class CreateDriverSchema(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    middle_name: str
    phone_number: str
    license_number: str


class UpdateDriverLocationSchema(BaseModel):
    coordinates: tuple[float, float]


class ResponseDriverForOrder(BaseModel):
    id: UUID
    phone_number: str
    first_name: str


class ResponseDriverSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str | None = None
    license_number: str
    phone_number: str
    completed_orders_count: int
    cancelled_orders_count: int
    status: DriverStatus
    on_shift: bool
    on_order: bool
    created_at: datetime

    @classmethod
    def from_domain(cls, driver: Driver) -> "ResponseDriverSchema":
        return cls(
            id=driver.id,
            first_name=driver.first_name,
            last_name=driver.last_name,
            middle_name=driver.middle_name,
            license_number=driver.license_number,
            phone_number=driver.phone_number.value,
            completed_orders_count=driver.completed_orders_count,
            cancelled_orders_count=driver.cancelled_orders_count,
            status=driver.status,
            on_shift=driver.on_shift,
            on_order=driver.on_order,
            created_at=driver.created_at,
        )
