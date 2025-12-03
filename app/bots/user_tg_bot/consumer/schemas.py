from uuid import UUID
from pydantic import BaseModel

from app.domain.enums.order_status import OrderStatus


class DriverAssignedToOrderEventSchema(BaseModel):
    order_id: UUID
    customer_id: UUID
    driver_id: UUID


class UpdateOrderStatusEventSchema(BaseModel):
    order_id: UUID
    customer_id: UUID
    driver_id: UUID
    status: OrderStatus


class CancelOrderEventSchema(BaseModel):
    order_id: UUID
    customer_id: UUID
    driver_id: UUID | None = None
    reason: str
