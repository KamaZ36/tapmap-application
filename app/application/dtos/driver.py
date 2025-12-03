from datetime import datetime
from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.driver_status import DriverStatus


@dataclass(frozen=True, eq=False, kw_only=True)
class DriverForOrderDTO:
    id: UUID
    first_name: str
    middle_name: str | None = None
    phone_number: str


@dataclass(frozen=True, eq=False, kw_only=True)
class DriverDTO:
    id: UUID

    first_name: str
    last_name: str
    middle_name: str | None = None

    phone_number: str
    license_number: str

    completed_orders_count: int
    cancelled_orders_count: int

    status: DriverStatus

    on_shift: bool
    on_order: bool

    created_at: datetime
