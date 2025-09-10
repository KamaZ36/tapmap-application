from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from app.domain.entities.driver import Driver
from app.domain.entities.user import User
from app.domain.entities.vehicle import Vehicle
from app.domain.enums.order_status import OrderStatus
from app.domain.value_objects.money import Money
from app.domain.value_objects.order_comment import OrderComment
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.order_point import OrderPoint


@dataclass(frozen=True)
class GetOrdersFilters:
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
class ExtendedOrder:
    id: UUID
    customer: User
    driver: Driver | None = None
    city_id: UUID
    vehicle: Vehicle | None = None
    points: list[OrderPoint]
    status: OrderStatus
    price: Money
    service_commission: Money
    travel_time: int
    travel_distance: int
    feeding_time: int | None = None
    feeding_distance: int | None = None
    comment: OrderComment | None = None
    created_at: datetime
