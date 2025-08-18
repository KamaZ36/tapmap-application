from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class VehicleNotFound(LogicException):
    
    @property
    def message(self) -> str:
        return "Транспорт не найден"
