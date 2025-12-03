from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.order import OrderDTO
from app.application.exceptions.order import OrderNotFound

from app.application.queries.base import Query, QueryHandler
from app.infrastructure.readers.draft_order.base import BaseDraftOrderReader
from app.infrastructure.readers.order.base import BaseOrderReader


@dataclass(frozen=True, eq=False)
class GetActiveOrderForCustomerQuery(Query):
    current_user_id: UUID
    customer_id: UUID


@dataclass(frozen=True, eq=False)
class GetActiveOrderForCustomerQueryHandler(
    QueryHandler[GetActiveOrderForCustomerQuery, OrderDTO]
):
    draft_order_reader: BaseDraftOrderReader
    order_reader: BaseOrderReader

    async def __call__(self, query: GetActiveOrderForCustomerQuery) -> OrderDTO:
        order = await self.draft_order_reader.get_by_customer_id(query.customer_id)
        if order is None:
            order = await self.order_reader.get_active_for_customer(query.customer_id)
        if order is None:
            raise OrderNotFound()
        return order
