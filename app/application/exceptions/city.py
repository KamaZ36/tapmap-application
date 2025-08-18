from dataclasses import dataclass

from app.application.exceptions.base import LogicException


class CityNotFound(LogicException):
    
    @property
    def message(self) -> str:
        return "Город не найден среди поддерживаемых."
