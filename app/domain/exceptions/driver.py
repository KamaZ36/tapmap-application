from dataclasses import dataclass

from app.domain.exceptions.base import AppException


@dataclass
class DriverIsNotOrder(AppException):
    @property
    def message(self) -> str:
        return "Водитель не выполняет заказ"


@dataclass
class DriverAlreadyOnShift(AppException):
    @property
    def message(self) -> str:
        return "Водитель уже на смене"


@dataclass
class DriverIsNotShift(AppException):
    @property
    def message(self) -> str:
        return "Водитель не на смене"


@dataclass
class DriverAlreadyOnOrder(AppException):
    @property
    def message(self) -> str:
        return "Водитель уже на заказе"


@dataclass
class DriverIsBlocked(AppException):
    @property
    def message(self) -> str:
        return "Водитель заблокирован"
