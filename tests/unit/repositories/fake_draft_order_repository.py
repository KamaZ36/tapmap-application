from uuid import UUID
from app.domain.entities.draft_order import DraftOrder
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository


class FakeDraftOrderRepository(BaseDraftOrderRepository):
    def __init__(self) -> None:
        self._draft_orders: dict[UUID, DraftOrder]
        self._draft_orders_by_customer: dict[UUID, DraftOrder]

    async def create(self, draft_order: DraftOrder) -> None:
        self._draft_orders[draft_order.id] = draft_order
        self._draft_orders_by_customer[draft_order.customer_id] = draft_order

    async def get_by_customer_id(self, customer_id: UUID) -> DraftOrder | None:
        draft_order = self._draft_orders_by_customer.get(customer_id, None)
        return draft_order

    async def update(self, draft_order: DraftOrder) -> None:
        self._draft_orders[draft_order.id] = draft_order
        self._draft_orders_by_customer[draft_order.customer_id] = draft_order

    async def delete(self, customer_id: UUID) -> None:
        draft_order = await self.get_by_customer_id(customer_id)
        self._draft_orders.pop(draft_order.id, None)
        self._draft_orders_by_customer.pop(customer_id, None)
