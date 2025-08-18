from uuid import UUID

from app.domain.entities.order import Order, OrderStatus
from app.infrastructure.repositories.order.base import BaseOrderRepository


class FakeOrderRepository(BaseOrderRepository):
    
    def __init__(self) -> None:
        self._orders: dict[UUID, Order]
        
    async def create(self, order: Order) -> None:
        self._orders[order.id] = order
    
    async def get_by_id(self, order_id: UUID) -> Order | None:
        order = self._orders.get(order_id, None)
        return order
    
    async def get_active_for_customer(self, customer_id: UUID) -> Order | None:
        active_statuses = (
            OrderStatus.driver_search, 
            OrderStatus.waiting_driver, 
            OrderStatus.driver_waiting_customer, 
            OrderStatus.processing
        )
        for order in self._orders.values():
            if (order.customer_id == customer_id and order.status in active_statuses):
                return order
        return None
    
    async def get_active_for_driver(self, driver_id: UUID) -> Order | None:
        active_statuses = {
            OrderStatus.waiting_driver,
            OrderStatus.driver_waiting_customer,
            OrderStatus.processing
        }
        for order in self._orders.values():
            if (order.driver_id == driver_id and order.status in active_statuses):
                return order
        return None
        
    async def update(self, order: Order) -> None:
        self._orders[order.id] = order
    