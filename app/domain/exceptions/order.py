from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.order_status import OrderStatus
from app.domain.exceptions.base import AppException


@dataclass(frozen=True)
class InvalidOrderStatusTransition(AppException):
    current_status: OrderStatus
    new_status: OrderStatus | None

    @property
    def message(self) -> str:
        return (
            f"Некорректный переход статуса: {self.current_status} -> {self.new_status}"
        )


@dataclass(frozen=True)
class DriverAlreadyAssignedToOrder(AppException):
    order_id: UUID
    assigned_driver: UUID

    @property
    def message(self) -> str:
        return f"На заказ {str(self.order_id)} уже назначен водитель {str(self.assigned_driver)}."


@dataclass(frozen=True)
class OrderCannotTwoPoints(AppException):
    @property
    def message(self) -> str:
        return f"В заказе должно присутствовать минимум 2 точки."


@dataclass(frozen=True, eq=False)
class OrderCannotBeConfirmedWithoutPriceError(Exception):
    @property
    def message(self) -> str:
        return "Невозможно подтвердить заказ без расчета цены."
