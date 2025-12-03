from uuid import UUID

from sqlalchemy import and_, between, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.enums.order_status import OrderStatus

from app.application.dtos.order import GetOrdersListFilters, OrderDTO, OrderForListDTO

from app.infrastructure.database.models.order import OrderModel
from app.infrastructure.readers.order.base import BaseOrderReader
from app.infrastructure.readers.order.converter import (
    convert_order_to_dto,
    convert_order_to_order_for_list,
)


class SQLOrderReader(BaseOrderReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, order_id: UUID) -> OrderDTO | None:
        query = (
            select(OrderModel)
            .options(selectinload(OrderModel.customer), selectinload(OrderModel.driver))
            .where(OrderModel.id == order_id)
        )

        result = await self._session.execute(query)
        order_model = result.scalar_one_or_none()
        return convert_order_to_dto(order_model) if order_model else None

    async def get_active_for_customer(self, customer_id: UUID) -> OrderDTO | None:
        query = (
            select(OrderModel)
            .where(
                OrderModel.customer_id == customer_id,
                OrderModel.status.in_(
                    [
                        OrderStatus.draft.value,
                        OrderStatus.driver_search.value,
                        OrderStatus.waiting_driver.value,
                        OrderStatus.driver_waiting_customer.value,
                        OrderStatus.processing.value,
                    ]
                ),
            )
            .options(selectinload(OrderModel.driver), selectinload(OrderModel.customer))
            .limit(1)
        )
        result = await self._session.execute(query)
        order_model = result.scalar_one_or_none()
        return convert_order_to_dto(order_model) if order_model else None

    async def get_list_with_filters(
        self, filters: GetOrdersListFilters
    ) -> list[OrderForListDTO]:
        query = select(OrderModel.id, OrderModel.created_at)

        conditions = []

        for field in ["customer_id", "driver_id", "city_id", "status"]:
            if value := getattr(filters, field):
                conditions.append(getattr(OrderModel, field) == value)

        range_filters = {
            "price": ("price_min", "price_max"),
            "travel_distance": ("travel_distance_min", "travel_distance_max"),
            "travel_time": ("travel_time_min", "travel_time_max"),
        }

        for field, (min_attr, max_attr) in range_filters.items():
            min_val = getattr(filters, min_attr)
            max_val = getattr(filters, max_attr)

            if min_val is not None and max_val is not None:
                conditions.append(between(getattr(OrderModel, field), min_val, max_val))
            elif min_val is not None:
                conditions.append(getattr(OrderModel, field) >= min_val)
            elif max_val is not None:
                conditions.append(getattr(OrderModel, field) <= max_val)

        if conditions:
            query = query.where(and_(*conditions))

        if filters.limit:
            query = query.limit(filters.limit)
        if filters.offset:
            query = query.offset(filters.offset)

        result = await self._session.execute(query)
        order_models = result.scalars().all()
        orders = [convert_order_to_order_for_list(order) for order in order_models]
        return orders
