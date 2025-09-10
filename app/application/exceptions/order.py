from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class OrderNotFound(LogicException):
    error_code: str = "ORDER_NOT_FOUND"

    @property
    def message(self) -> str:
        return "Заказ не найден."
