from dataclasses import dataclass
from app.application.exceptions.base import LogicException


@dataclass(frozen=True)
class DriverNotFound(LogicException):
    error_code: str = "DRIVER_NOT_FOUND"

    @property
    def message(self) -> str:
        return "Водитель не найден"


@dataclass(frozen=True)
class DriverLastLocationNotSet(LogicException):
    error_code: str = "DRIVER_LAST_LOCATION_NOT_SET"

    @property
    def message(self) -> str:
        return "Последнее местоположение водителя не установлено"
