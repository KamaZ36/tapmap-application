from dataclasses import asdict
from uuid import UUID

from sqlalchemy import ScalarResult, and_, between, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.order import GetOrdersFilters
from app.application.exceptions.order import OrderNotFound
from app.infrastructure.database.models.order import OrderModel
from app.infrastructure.repositories.order.base import BaseOrderRepository

from app.domain.entities.order import Order, OrderStatus


class SQLAlchemyOrderRepository(BaseOrderRepository): 
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, order: Order) -> None:
        order_model = OrderModel.create(order)
        self.session.add(order_model)
        
    async def get_by_id(self, order_id: UUID) -> Order:
        query = select(OrderModel).where(OrderModel.id == order_id)
        result = await self.session.execute(query)
        order_model: OrderModel | None = result.scalar_one_or_none()
        if order_model is None:
            raise OrderNotFound()
        return order_model.to_entity()
        
    async def get_filtered_orders(self, filters: GetOrdersFilters) -> list[Order]:
        query = select(OrderModel)
        
        conditions = []
        
        for field in ['customer_id', 'driver_id', 'city_id', 'status']:
            if value := getattr(filters, field):
                conditions.append(getattr(OrderModel, field) == value)
            
        range_filters = {
            'price': ('price_min', 'price_max'),
            'travel_distance': ('travel_distance_min', 'travel_distance_max'),
            'travel_time': ('travel_time_min', 'travel_time_max')
        }
        
        for field, (min_attr, max_attr) in range_filters.items():
            min_val = getattr(filters, min_attr)
            max_val = getattr(filters, max_attr)
            
            if min_val is not None and max_val is not None:
                conditions.append(between(getattr(Order, field), min_val, max_val))
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
        
        result = await self.session.execute(query)
        order_models: ScalarResult[OrderModel] | None = result.scalars()
        orders = [order.to_entity() for order in order_models]
        return orders
        
        
    async def get_active_for_customer(self, customer_id: UUID) -> Order: 
        query = select(OrderModel).where(
            OrderModel.customer_id == customer_id, 
            OrderModel.status.in_(
                [
                    OrderStatus.driver_search.value, 
                    OrderStatus.waiting_driver.value, 
                    OrderStatus.driver_waiting_customer.value, 
                    OrderStatus.processing.value
                ]
            )
        ).limit(1)
        result = await self.session.execute(query)
        order_model: OrderModel | None = result.scalar_one_or_none()
        if order_model is None:
            raise OrderNotFound()
        return order_model.to_entity()
    
    async def get_active_for_driver(self, driver_id: UUID) -> Order: 
        query = select(OrderModel).where(
            OrderModel.driver_id == driver_id, 
            OrderModel.status.in_(
                [ 
                    OrderStatus.waiting_driver.value, 
                    OrderStatus.driver_waiting_customer.value, 
                    OrderStatus.processing.value
                ]
            )
        )
        result = await self.session.execute(query)
        order_model: OrderModel | None = result.scalar_one_or_none()
        if order_model is None:
            raise OrderNotFound()
        return order_model.to_entity()

    async def update(self, order: Order) -> None: 
        stmt = (
            update(OrderModel)
            .where(OrderModel.id == order.id)
            .values(
                driver_id=order.driver_id,
                points=[asdict(point) for point in order.points],
                status=order.status,
                price=order.price.value,
                service_commission=order.service_commission.value,
                travel_distance=order.travel_distance,
                travel_time=order.travel_time,
                feeding_distance=order.feeding_distance,
                feeding_time=order.feeding_time,
                comment=order.comment.text if order.comment else None
            )
        )
        await self.session.execute(stmt)
