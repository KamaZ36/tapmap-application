from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.order import OrderDTO
from app.application.exceptions.order import OrderNotFound
from app.application.queries.base import Query, QueryHandler
from app.infrastructure.readers.order.base import BaseOrderReader


@dataclass(frozen=True, eq=False)
class GetActiveOrderForDirverQuery(Query):
    driver_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, eq=False)
class GetActiveOrderForDriverQueryHandler(
    QueryHandler[GetActiveOrderForDirverQuery, OrderDTO]
):
    order_reader: BaseOrderReader

    async def __call__(self, query: GetActiveOrderForDirverQuery) -> OrderDTO:
        order = await self.order_reader.get_active_for_driver(driver_id=query.driver_id)
        if order is None:
            raise OrderNotFound()

        return order
