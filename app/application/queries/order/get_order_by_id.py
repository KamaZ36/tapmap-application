from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.order import OrderDTO
from app.application.exceptions.order import OrderNotFound

from app.application.queries.base import Query, QueryHandler
from app.infrastructure.readers.draft_order.base import BaseDraftOrderReader
from app.infrastructure.readers.order.base import BaseOrderReader


@dataclass(frozen=True, eq=False)
class GetOrderByIdQuery(Query):
    current_user_id: UUID
    order_id: UUID


@dataclass
class GetOrderByIdQueryHandler(QueryHandler[GetOrderByIdQuery, OrderDTO]):
    order_reader: BaseOrderReader
    draft_order_reader: BaseDraftOrderReader

    async def __call__(self, query: GetOrderByIdQuery) -> OrderDTO:
        order = await self.draft_order_reader.get_by_id(query.order_id)
        if order is None:
            order = await self.order_reader.get_by_id(query.order_id)

        if order is None:
            raise OrderNotFound()

        return order
