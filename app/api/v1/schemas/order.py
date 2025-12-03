from dataclasses import asdict
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.api.v1.schemas.user import ResponseCustomerForOrderSchema
from app.domain.entities.order import Order, OrderStatus

from app.application.dtos.order import OrderDTO

from app.api.v1.schemas.driver import (
    ResponseDriverForOrderSchema,
)
from app.api.v1.schemas.vehicle import ResponseVehicleForOrder


class CreateOrderSchema(BaseModel):
    start_point: str | tuple[float, float]


class AddPointToOrderSchema(BaseModel):
    point: str | tuple[float, float]


class AddCommentToOrderSchema(BaseModel):
    comment: str


class CancelOrderSchema(BaseModel):
    reason: str


class GetOrderSFiltersSchema(BaseModel):
    customer_id: Optional[UUID] = None
    driver_id: Optional[UUID] = None
    city_id: Optional[UUID] = None
    status: Optional[OrderStatus] = None
    price_min: Optional[Decimal] = None
    price_max: Optional[Decimal] = None
    travel_distance_min: Optional[int] = None
    travel_distance_max: Optional[int] = None
    travel_time_min: Optional[int] = None
    travel_time_max: Optional[int] = None
    limit: Optional[int] = 5
    offset: Optional[int] = 0


class ResponseExtendedOrderSchema(BaseModel):
    id: UUID
    customer: ResponseCustomerForOrderSchema
    driver: ResponseDriverForOrderSchema | None = None
    city_id: UUID
    vehicle: ResponseVehicleForOrder | None = None
    points: list[dict[str, Any]]
    status: OrderStatus
    price: Decimal
    service_commission: Decimal
    travel_time: int
    travel_distance: int
    feeding_time: int | None = None
    feeding_distance: int | None = None
    comment: str | None = None
    created_at: datetime

    @classmethod
    def from_domain(cls, order: OrderDTO) -> "ResponseExtendedOrderSchema":
        driver_for_order_schema = None

        if order.driver:
            driver_for_order_schema = ResponseDriverForOrderSchema.from_dto(
                order.driver
            )

        customer_for_order_schema = ResponseCustomerForOrderSchema.from_dto(
            order.customer
        )

        order_schema = cls(
            id=order.id,
            customer=customer_for_order_schema,
            driver=driver_for_order_schema,
            city_id=order.city_id,
            vehicle=ResponseVehicleForOrder(
                id=order.vehicle.id,
                brand=order.vehicle.brand,
                model=order.vehicle.model,
                color=order.vehicle.color,
                number=order.vehicle.number.value,
            )
            if order.vehicle
            else None,
            points=[asdict(point) for point in order.points],
            status=order.status,
            price=order.price.value,
            service_commission=order.service_commission.value,
            travel_time=order.travel_time,
            travel_distance=order.travel_distance,
            feeding_distance=order.feeding_distance,
            feeding_time=order.feeding_time,
            comment=order.comment.text if order.comment else None,
            created_at=order.created_at,
        )
        return order_schema


class ResponseOrderSchema(BaseModel):
    id: UUID
    customer_id: UUID
    driver_id: UUID | None = None
    city_id: UUID
    points: list[dict[str, Any]]
    status: OrderStatus
    price: Decimal
    service_commission: Decimal
    travel_time: int
    travel_distance: int
    comment: str | None = None
    created_at: datetime

    @classmethod
    def from_domain(cls, order: Order) -> "ResponseOrderSchema":
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            driver_id=order.driver_id if order.driver_id else None,
            city_id=order.city_id,
            points=[asdict(point) for point in order.points],
            status=order.status,
            price=order.price.value,
            service_commission=order.service_commission.value,
            travel_time=order.travel_time,
            travel_distance=order.travel_distance,
            comment=order.comment.text if order.comment else None,
            created_at=order.created_at,
        )
