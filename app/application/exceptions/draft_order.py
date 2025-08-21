from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class DraftOrderNotFound(LogicException):
    error_code: str = "DRAFT_ORDER_NOT_FOUND"
    
    @property
    def message(self) -> str:
        return "Черновик заказа не найден"


@dataclass(kw_only=True)
class InvalidLocation(LogicException):
    error_code: str = "INVALID_LOCATION"
    location: str | tuple[float, float]
    
    @property
    def message(self) -> str:
        return f"Не удалось распознать адрес или координаты: {self.location}"
