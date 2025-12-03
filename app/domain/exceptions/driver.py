from dataclasses import dataclass

from app.domain.exceptions.base import AppException


@dataclass(frozen=True)
class DriverIsNotOrder(AppException):
    @property
    def message(self) -> str:
        return "Водитель не выполняет заказ"


@dataclass(frozen=True)
class DriverAlreadyOnShift(AppException):
    @property
    def message(self) -> str:
        return "Водитель уже на смене"


@dataclass(frozen=True)
class DriverIsNotShift(AppException):
    @property
    def message(self) -> str:
        return "Водитель не на смене"


@dataclass(frozen=True)
class DriverAlreadyOnOrder(AppException):
    @property
    def message(self) -> str:
        return "Водитель уже на заказе"


@dataclass(frozen=True)
class DriverIsBlocked(AppException):
    @property
    def message(self) -> str:
        return "Водитель заблокирован"
