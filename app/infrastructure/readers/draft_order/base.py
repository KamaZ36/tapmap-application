from typing import Protocol
from uuid import UUID

from app.application.dtos.order import OrderDTO


class BaseDraftOrderReader(Protocol):
    async def get_by_id(self, order_id: UUID) -> OrderDTO | None: ...

    async def get_by_customer_id(self, customer_id: UUID) -> OrderDTO | None: ...
