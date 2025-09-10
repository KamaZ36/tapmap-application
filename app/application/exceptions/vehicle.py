from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass
class VehicleNotFound(LogicException):
    error_code: str = "VEHICLE_NOT_FOUND"

    @property
    def message(self) -> str:
        return "Транспорт не найден"
