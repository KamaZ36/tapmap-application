from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class OrderNotFound(LogicException):
    
    @property
    def message(self) -> str:
        return "Заказ не найден."
