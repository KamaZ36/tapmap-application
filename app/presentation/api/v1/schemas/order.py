from dataclasses import asdict
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.domain.entities.order import Order, OrderStatus

from app.application.dtos.order import ExtendedOrder

from app.presentation.api.v1.schemas.driver import ResponseDriverForOrder
from app.presentation.api.v1.schemas.user import ResponseUserForOrder
from app.presentation.api.v1.schemas.vehicle import ResponseVehicleForOrder


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


class CancelOrderSchema(BaseModel):
    reason: str


class ResponseExtendedOrderSchema(BaseModel):
    id: UUID
    customer: ResponseUserForOrder
    driver: ResponseDriverForOrder | None = None
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
    def from_domain(
        cls, extended_order: ExtendedOrder
    ) -> "ResponseExtendedOrderSchema":
        extended_order_schema = cls(
            id=extended_order.id,
            customer=ResponseUserForOrder(
                id=extended_order.customer.id,
                name=extended_order.customer.name,
                phone_number=extended_order.customer.phone_number.value,
            ),
            driver=ResponseDriverForOrder(
                id=extended_order.driver.id,
                phone_number=extended_order.driver.phone_number.value,
                first_name=extended_order.driver.first_name,
            )
            if extended_order.driver
            else None,
            city_id=extended_order.city_id,
            vehicle=ResponseVehicleForOrder(
                id=extended_order.vehicle.id,
                brand=extended_order.vehicle.brand,
                model=extended_order.vehicle.model,
                color=extended_order.vehicle.color,
                number=extended_order.vehicle.number.value,
            )
            if extended_order.vehicle
            else None,
            points=[asdict(point) for point in extended_order.points],
            status=extended_order.status,
            price=extended_order.price.value,
            service_commission=extended_order.service_commission.value,
            travel_time=extended_order.travel_time,
            travel_distance=extended_order.travel_distance,
            feeding_distance=extended_order.feeding_distance,
            feeding_time=extended_order.feeding_time,
            comment=extended_order.comment.text if extended_order.comment else None,
            created_at=extended_order.created_at,
        )
        return extended_order_schema


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
