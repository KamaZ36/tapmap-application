from dataclasses import dataclass

from app.application.exceptions.base import LogicException


@dataclass(frozen=True)
class CityNotSupported(LogicException):
    error_code: str = "CITY_NOT_SUPPORTED"

    @property
    def message(self) -> str:
        return f"Указанное место не поддерживается сервисом."


@dataclass(frozen=True)
class CityNotFound(LogicException):
    error_code: str = "CITY_NOT_FOUND"

    @property
    def message(self) -> str:
        return "Город не найден"
