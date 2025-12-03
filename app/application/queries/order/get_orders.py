from dataclasses import dataclass
from uuid import UUID

from app.application.queries.base import Query, QueryHandler
from app.infrastructure.readers.order.base import BaseOrderReader

from app.application.dtos.order import GetOrdersListFilters, OrderForListDTO


@dataclass(frozen=True, eq=False)
class GetOrdersListQuery(Query):
    current_user_id: UUID
    filters: GetOrdersListFilters


@dataclass
class GetOrdersListQueryHandler(
    QueryHandler[GetOrdersListQuery, list[OrderForListDTO]]
):
    order_reader: BaseOrderReader

    async def __call__(self, query: GetOrdersListQuery) -> list[OrderForListDTO]:
        orders = await self.order_reader.get_list_with_filters(query.filters)
        return orders
