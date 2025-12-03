from dataclasses import dataclass
from typing import Any
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from app.domain.enums.order_status import OrderStatus
from app.domain.value_objects.order_point import OrderPoint

from app.application.dtos.driver import DriverForOrderDTO
from app.application.dtos.user import UserForOrderDTO
from app.application.dtos.vehicle import VehicleForOrderDTO


@dataclass(frozen=True)
class GetOrdersListFilters:
    customer_id: UUID | None = None
    driver_id: UUID | None = None
    city_id: UUID | None = None
    status: OrderStatus | None = None
    price_min: Decimal | None = None
    price_max: Decimal | None = None
    travel_distance_min: int | None = None
    travel_distance_max: int | None = None
    travel_time_min: int | None = None
    travel_time_max: int | None = None
    limit: int | None = 5
    offset: int | None = 0


@dataclass(frozen=True, kw_only=True)
class OrderDTO:
    id: UUID
    customer: UserForOrderDTO
    driver: DriverForOrderDTO | None = None
    city_id: UUID
    vehicle: VehicleForOrderDTO | None = None
    points: list[OrderPoint]
    status: OrderStatus
    price: Decimal | None
    service_commission: Decimal | None
    travel_time: int | None
    travel_distance: int | None
    feeding_time: int | None = None
    feeding_distance: int | None = None
    comment: str | None = None
    created_at: datetime


@dataclass(frozen=True, eq=False, kw_only=True)
class OrderForListDTO:
    id: UUID
    created_at: datetime
