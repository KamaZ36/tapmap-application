from typing import Protocol
from uuid import UUID

from app.application.dtos.order import GetOrdersListFilters, OrderDTO, OrderForListDTO


class BaseOrderReader(Protocol):
    async def get_by_id(self, order_id: UUID) -> OrderDTO | None: ...

    async def get_active_for_customer(self, customer_id: UUID) -> OrderDTO | None: ...

    async def get_active_for_driver(self, driver_id: UUID) -> OrderDTO | None: ...

    async def get_list_with_filters(
        self, filters: GetOrdersListFilters
    ) -> list[OrderForListDTO]: ...
