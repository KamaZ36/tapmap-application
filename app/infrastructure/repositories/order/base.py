from typing import Protocol
from uuid import UUID

from app.application.dtos.order import GetOrdersFilters
from app.domain.entities.order import Order


class BaseOrderRepository(Protocol): 
    
    async def create(self, order: Order) -> None: ...
    
    async def get_by_id(self, order_id: UUID) -> Order: ...
    
    async def get_filtered_orders(self, filters: GetOrdersFilters) -> list[Order]: ...
    
    async def get_active_for_customer(self, customer_id: UUID) -> Order: ...

    async def get_active_for_driver(self, driver_id: UUID) -> Order: ...

    async def update(self, order: Order) -> None: ...
