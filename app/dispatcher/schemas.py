from uuid import UUID
from pydantic import BaseModel


class OrderConfirmedEvent(BaseModel):
    order_id: UUID
