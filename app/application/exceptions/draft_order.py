from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class DraftOrderNotFound(LogicException):
    
    @property
    def message(self) -> str:
        return "Черновик заказа не найден"
